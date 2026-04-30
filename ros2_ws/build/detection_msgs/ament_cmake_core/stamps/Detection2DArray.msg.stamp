# Header with timestamp and frame_id
std_msgs/Header header

# Array of detections for this frame
Detection2D[] detections

# Performance metrics
float32 inference_latency_ms   # time taken for YOLO inference only
float32 total_latency_ms       # time from image received to message published
float32 fps                    # frames per second (rolling average)
