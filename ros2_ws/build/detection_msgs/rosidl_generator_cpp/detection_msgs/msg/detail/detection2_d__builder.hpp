// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d.hpp"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__BUILDER_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "detection_msgs/msg/detail/detection2_d__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace detection_msgs
{

namespace msg
{

namespace builder
{

class Init_Detection2D_confidence
{
public:
  explicit Init_Detection2D_confidence(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  ::detection_msgs::msg::Detection2D confidence(::detection_msgs::msg::Detection2D::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_class_id
{
public:
  explicit Init_Detection2D_class_id(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_confidence class_id(::detection_msgs::msg::Detection2D::_class_id_type arg)
  {
    msg_.class_id = std::move(arg);
    return Init_Detection2D_confidence(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_class_name
{
public:
  explicit Init_Detection2D_class_name(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_class_id class_name(::detection_msgs::msg::Detection2D::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_Detection2D_class_id(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_y_max
{
public:
  explicit Init_Detection2D_y_max(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_class_name y_max(::detection_msgs::msg::Detection2D::_y_max_type arg)
  {
    msg_.y_max = std::move(arg);
    return Init_Detection2D_class_name(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_x_max
{
public:
  explicit Init_Detection2D_x_max(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_y_max x_max(::detection_msgs::msg::Detection2D::_x_max_type arg)
  {
    msg_.x_max = std::move(arg);
    return Init_Detection2D_y_max(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_y_min
{
public:
  explicit Init_Detection2D_y_min(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_x_max y_min(::detection_msgs::msg::Detection2D::_y_min_type arg)
  {
    msg_.y_min = std::move(arg);
    return Init_Detection2D_x_max(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_x_min
{
public:
  Init_Detection2D_x_min()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Detection2D_y_min x_min(::detection_msgs::msg::Detection2D::_x_min_type arg)
  {
    msg_.x_min = std::move(arg);
    return Init_Detection2D_y_min(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::detection_msgs::msg::Detection2D>()
{
  return detection_msgs::msg::builder::Init_Detection2D_x_min();
}

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__BUILDER_HPP_
