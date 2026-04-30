// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d_array.hpp"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__BUILDER_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "detection_msgs/msg/detail/detection2_d_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace detection_msgs
{

namespace msg
{

namespace builder
{

class Init_Detection2DArray_fps
{
public:
  explicit Init_Detection2DArray_fps(::detection_msgs::msg::Detection2DArray & msg)
  : msg_(msg)
  {}
  ::detection_msgs::msg::Detection2DArray fps(::detection_msgs::msg::Detection2DArray::_fps_type arg)
  {
    msg_.fps = std::move(arg);
    return std::move(msg_);
  }

private:
  ::detection_msgs::msg::Detection2DArray msg_;
};

class Init_Detection2DArray_total_latency_ms
{
public:
  explicit Init_Detection2DArray_total_latency_ms(::detection_msgs::msg::Detection2DArray & msg)
  : msg_(msg)
  {}
  Init_Detection2DArray_fps total_latency_ms(::detection_msgs::msg::Detection2DArray::_total_latency_ms_type arg)
  {
    msg_.total_latency_ms = std::move(arg);
    return Init_Detection2DArray_fps(msg_);
  }

private:
  ::detection_msgs::msg::Detection2DArray msg_;
};

class Init_Detection2DArray_inference_latency_ms
{
public:
  explicit Init_Detection2DArray_inference_latency_ms(::detection_msgs::msg::Detection2DArray & msg)
  : msg_(msg)
  {}
  Init_Detection2DArray_total_latency_ms inference_latency_ms(::detection_msgs::msg::Detection2DArray::_inference_latency_ms_type arg)
  {
    msg_.inference_latency_ms = std::move(arg);
    return Init_Detection2DArray_total_latency_ms(msg_);
  }

private:
  ::detection_msgs::msg::Detection2DArray msg_;
};

class Init_Detection2DArray_detections
{
public:
  explicit Init_Detection2DArray_detections(::detection_msgs::msg::Detection2DArray & msg)
  : msg_(msg)
  {}
  Init_Detection2DArray_inference_latency_ms detections(::detection_msgs::msg::Detection2DArray::_detections_type arg)
  {
    msg_.detections = std::move(arg);
    return Init_Detection2DArray_inference_latency_ms(msg_);
  }

private:
  ::detection_msgs::msg::Detection2DArray msg_;
};

class Init_Detection2DArray_header
{
public:
  Init_Detection2DArray_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Detection2DArray_detections header(::detection_msgs::msg::Detection2DArray::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Detection2DArray_detections(msg_);
  }

private:
  ::detection_msgs::msg::Detection2DArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::detection_msgs::msg::Detection2DArray>()
{
  return detection_msgs::msg::builder::Init_Detection2DArray_header();
}

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__BUILDER_HPP_
