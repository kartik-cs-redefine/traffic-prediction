import cv2, math, datetime, os
import pandas as pd
from ultralytics import YOLO

# ---------------- SETTINGS ----------------
VIDEO_DIR = r"videos\AIC21-Track4-Anomaly-Detection\aic21-track4-train-data"
# video_id: (LINE_FRAC, ROI_FRAC)  -> preview dekh ke har video ke liye badalna
VIDEOS = {
    1: (0.75, 0.45),  11: (0.75, 0.4),  16: (0.8, 0.3),  26: (0.7, 0.3),
    41: (0.75, 0.4),  51: (0.75, 0.5),  56: (0.75, 0.4), 61: (0.75, 0.4),
    66: (0.75, 0.45), 81: (0.7, 0.4),   91: (0.75, 0.4), 96: (0.75, 0.45),
}
PREVIEW_ONLY = False
ONLY = [36]              
WINDOW_SEC = 5
SKIP = 2                 # slow ho to 3 kar
METER_PER_PIXEL = 0.05   # approximate (har camera ke liye alag hoga, calibrate nahi hai)
START_TIME = datetime.datetime(2026, 1, 1, 0, 0, 0)   # assumed
COLS = ["video_id", "timestamp", "car_count", "bus_count", "bike_count",
        "avg_speed", "density", "occupancy", "flow"]
# ------------------------------------------

os.makedirs("previews", exist_ok=True)
os.makedirs("out", exist_ok=True)


def vpath(vid):
    return os.path.join(VIDEO_DIR, f"{vid}.mp4")


def preview(vid, lf, rf):
    cap = cv2.VideoCapture(vpath(vid))
    ok, f = cap.read()
    cap.release()
    if not ok:
        print(vid, ": video nahi khula")
        return
    h, w = f.shape[:2]
    cv2.line(f, (0, int(h * lf)), (w, int(h * lf)), (0, 0, 255), 3)   # laal = count line
    cv2.line(f, (0, int(h * rf)), (w, int(h * rf)), (255, 0, 0), 2)   # neeli = ROI top
    cv2.putText(f, str(vid), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
    cv2.imwrite(os.path.join("previews", f"{vid}.jpg"), f)
    print("preview saved:", vid)


def process(vid, lf, rf):
    cap = cv2.VideoCapture(vpath(vid))
    if not cap.isOpened():
        print(vid, ": video nahi khula")
        return
    model = YOLO("yolov8n.pt")            # har video ke liye fresh (tracker reset)
    fps = cap.get(cv2.CAP_PROP_FPS)
    eff_fps = fps / SKIP
    window_frames = int(WINDOW_SEC * eff_fps)
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f"[{vid}] {total / fps:.0f} sec, expected rows ~{int(total / fps // WINDOW_SEC)}")

    line_y = roi_top = roi_area = None
    prev_pos, counted = {}, set()
    cars, bikes, buses = set(), set(), set()
    speeds, dens, occs = [], [], []
    crossings, proc_idx, rows = 0, 0, []

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        for _ in range(SKIP - 1):
            cap.grab()
        h, w = frame.shape[:2]
        if line_y is None:
            line_y, roi_top = int(h * lf), int(h * rf)
            roi_area = w * (h - roi_top)
        proc_idx += 1

        r = model.track(frame, persist=True, tracker="bytetrack.yaml",
                        classes=[2, 3, 5, 7], verbose=False)[0]
        n_in, area_in = 0, 0
        if r.boxes.id is not None:
            ids = r.boxes.id.int().tolist()
            clss = r.boxes.cls.int().tolist()
            for tid, c, (x1, y1, x2, y2) in zip(ids, clss, r.boxes.xyxy.tolist()):
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                if cy > roi_top:
                    n_in += 1
                    area_in += (x2 - x1) * (y2 - y1)
                    if c in (2, 7): cars.add(tid)
                    elif c == 3:    bikes.add(tid)
                    elif c == 5:    buses.add(tid)
                if tid in prev_pos:
                    px, py = prev_pos[tid]
                    if cy > roi_top:
                        speeds.append(math.hypot(cx - px, cy - py)
                                      * eff_fps * METER_PER_PIXEL * 3.6)
                    if tid not in counted and ((py < line_y <= cy) or (py >= line_y > cy)):
                        crossings += 1
                        counted.add(tid)
                prev_pos[tid] = (cx, cy)
        dens.append(n_in)
        occs.append(area_in / roi_area)

        if proc_idx % window_frames == 0:
            n = proc_idx // window_frames
            ts = START_TIME + datetime.timedelta(seconds=WINDOW_SEC * n)
            rows.append({
                "video_id": vid,
                "timestamp": ts.isoformat(timespec="seconds"),
                "car_count": len(cars), "bus_count": len(buses), "bike_count": len(bikes),
                "avg_speed": round(sum(speeds) / len(speeds), 2) if speeds else 0,
                "density": round(sum(dens) / len(dens), 2),
                "occupancy": round(sum(occs) / len(occs), 4),
                "flow": round(crossings * 60 / WINDOW_SEC, 1),
            })
            cars.clear(); bikes.clear(); buses.clear()
            speeds.clear(); dens.clear(); occs.clear()
            crossings = 0
            if n % 20 == 0:
                print(f"  [{vid}] {n} rows")

    cap.release()
    pd.DataFrame(rows, columns=COLS).to_csv(os.path.join("out", f"{vid}.csv"), index=False)
    print(f"[{vid}] done, {len(rows)} rows saved")


for vid, (lf, rf) in VIDEOS.items():
    if ONLY and vid not in ONLY:
        continue
    if PREVIEW_ONLY:
        preview(vid, lf, rf)
    elif os.path.exists(os.path.join("out", f"{vid}.csv")):
        print(vid, ": already done, skip")        # laptop band hua to resume ho jayega
    else:
        process(vid, lf, rf)

if not PREVIEW_ONLY:
    files = [os.path.join("out", f) for f in os.listdir("out") if f.endswith(".csv")]
    if files:
        all_df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
        all_df.to_csv("all_features.csv", index=False)
        print("all_features.csv:", len(all_df), "rows,", len(files), "videos")