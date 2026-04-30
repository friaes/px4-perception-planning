// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d.h"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_H_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'class_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Detection2D in the package detection_msgs.
/**
  * Bounding box
 */
typedef struct detection_msgs__msg__Detection2D
{
  float x_min;
  float y_min;
  float x_max;
  float y_max;
  /// Detected class label
  rosidl_runtime_c__String class_name;
  /// Class index
  int32_t class_id;
  /// Confidence score
  float confidence;
} detection_msgs__msg__Detection2D;

// Struct for a sequence of detection_msgs__msg__Detection2D.
typedef struct detection_msgs__msg__Detection2D__Sequence
{
  detection_msgs__msg__Detection2D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} detection_msgs__msg__Detection2D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_H_
