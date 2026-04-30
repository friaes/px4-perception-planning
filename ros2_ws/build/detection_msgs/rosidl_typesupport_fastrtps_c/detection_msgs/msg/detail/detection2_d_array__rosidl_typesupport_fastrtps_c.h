// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice
#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "detection_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "detection_msgs/msg/detail/detection2_d_array__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
bool cdr_serialize_detection_msgs__msg__Detection2DArray(
  const detection_msgs__msg__Detection2DArray * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
bool cdr_deserialize_detection_msgs__msg__Detection2DArray(
  eprosima::fastcdr::Cdr &,
  detection_msgs__msg__Detection2DArray * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t get_serialized_size_detection_msgs__msg__Detection2DArray(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t max_serialized_size_detection_msgs__msg__Detection2DArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
bool cdr_serialize_key_detection_msgs__msg__Detection2DArray(
  const detection_msgs__msg__Detection2DArray * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t get_serialized_size_key_detection_msgs__msg__Detection2DArray(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t max_serialized_size_key_detection_msgs__msg__Detection2DArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, detection_msgs, msg, Detection2DArray)();

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
