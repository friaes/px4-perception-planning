// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "detection_msgs/msg/detection2_d.hpp"


#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__detection_msgs__msg__Detection2D __attribute__((deprecated))
#else
# define DEPRECATED__detection_msgs__msg__Detection2D __declspec(deprecated)
#endif

namespace detection_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Detection2D_
{
  using Type = Detection2D_<ContainerAllocator>;

  explicit Detection2D_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x_min = 0.0f;
      this->y_min = 0.0f;
      this->x_max = 0.0f;
      this->y_max = 0.0f;
      this->class_name = "";
      this->class_id = 0l;
      this->confidence = 0.0f;
    }
  }

  explicit Detection2D_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : class_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x_min = 0.0f;
      this->y_min = 0.0f;
      this->x_max = 0.0f;
      this->y_max = 0.0f;
      this->class_name = "";
      this->class_id = 0l;
      this->confidence = 0.0f;
    }
  }

  // field types and members
  using _x_min_type =
    float;
  _x_min_type x_min;
  using _y_min_type =
    float;
  _y_min_type y_min;
  using _x_max_type =
    float;
  _x_max_type x_max;
  using _y_max_type =
    float;
  _y_max_type y_max;
  using _class_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _class_name_type class_name;
  using _class_id_type =
    int32_t;
  _class_id_type class_id;
  using _confidence_type =
    float;
  _confidence_type confidence;

  // setters for named parameter idiom
  Type & set__x_min(
    const float & _arg)
  {
    this->x_min = _arg;
    return *this;
  }
  Type & set__y_min(
    const float & _arg)
  {
    this->y_min = _arg;
    return *this;
  }
  Type & set__x_max(
    const float & _arg)
  {
    this->x_max = _arg;
    return *this;
  }
  Type & set__y_max(
    const float & _arg)
  {
    this->y_max = _arg;
    return *this;
  }
  Type & set__class_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->class_name = _arg;
    return *this;
  }
  Type & set__class_id(
    const int32_t & _arg)
  {
    this->class_id = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    detection_msgs::msg::Detection2D_<ContainerAllocator> *;
  using ConstRawPtr =
    const detection_msgs::msg::Detection2D_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::Detection2D_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::Detection2D_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__detection_msgs__msg__Detection2D
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__detection_msgs__msg__Detection2D
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Detection2D_ & other) const
  {
    if (this->x_min != other.x_min) {
      return false;
    }
    if (this->y_min != other.y_min) {
      return false;
    }
    if (this->x_max != other.x_max) {
      return false;
    }
    if (this->y_max != other.y_max) {
      return false;
    }
    if (this->class_name != other.class_name) {
      return false;
    }
    if (this->class_id != other.class_id) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    return true;
  }
  bool operator!=(const Detection2D_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Detection2D_

// alias to use template instance with default allocator
using Detection2D =
  detection_msgs::msg::Detection2D_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_HPP_
