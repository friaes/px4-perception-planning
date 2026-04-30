// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d_array.h"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_H_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'detections'
#include "detection_msgs/msg/detail/detection2_d__struct.h"

/// Struct defined in msg/Detection2DArray in the package detection_msgs.
/**
  * Header with timestamp and frame_id
 */
typedef struct detection_msgs__msg__Detection2DArray
{
  std_msgs__msg__Header header;
  /// Array of detections for this frame
  detection_msgs__msg__Detection2D__Sequence detections;
  /// Performance metrics
  /// time taken for YOLO inference only
  float inference_latency_ms;
  /// time from image received to message published
  float total_latency_ms;
  /// frames per second (rolling average)
  float fps;
} detection_msgs__msg__Detection2DArray;

// Struct for a sequence of detection_msgs__msg__Detection2DArray.
typedef struct detection_msgs__msg__Detection2DArray__Sequence
{
  detection_msgs__msg__Detection2DArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} detection_msgs__msg__Detection2DArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_H_
