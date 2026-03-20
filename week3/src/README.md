# ROS2 Publisher-Subscriber Exercise

This project contains a complete ROS2 setup with publisher and subscriber packages, custom message definitions, and parameterized launch files.

## Project Structure

```
src/
├── custom_publisher_package/       # Publisher node package
│   ├── custom_publisher_package/
│   │   ├── __init__.py
│   │   └── custom_publisher_node.py
│   ├── launch/
│   │   ├── publisher_launch.py
│   │   ├── subscriber_launch.py
│   │   └── combined_launch.py
│   ├── package.xml
│   └── CMakeLists.txt
├── custom_subscriber_package/      # Subscriber node package
│   ├── custom_subscriber_package/
│   │   ├── __init__.py
│   │   └── custom_subscriber_node.py
│   ├── launch/
│   │   └── subscriber_launch.py
│   ├── package.xml
│   └── CMakeLists.txt
├── custom_message_package/         # Custom message definitions
│   ├── msg/
│   │   └── CustomMessage.msg
│   ├── package.xml
│   └── CMakeLists.txt
└── README.md
```

## Packages

### 1. custom_publisher_package

**Node**: `custom_publisher_node`

Publishes messages to the `custom_topic` with the following specifications:
- Message Type: `example_interfaces/msg/String`
- Topic: `custom_topic` (configurable)
- Message Content: `custom_string` (configurable)
- Publishing Frequency: 1 Hz (configurable)

**Parameters**:
- `timer_frequency` (float): Publishing frequency in Hz (default: 1.0)
- `topic_name` (string): Topic to publish to (default: custom_topic)
- `message_content` (string): Message content (default: custom_string)

### 2. custom_subscriber_package

**Node**: `custom_subscriber_node`

Subscribes to messages from the `custom_topic` with the following specifications:
- Message Type: `example_interfaces/msg/String`
- Topic: `custom_topic` (configurable)
- Logging: INFO level logs to screen

**Parameters**:
- `topic_name` (string): Topic to subscribe to (default: custom_topic)

### 3. custom_message_package (Challenge I)

Defines a custom message type `CustomMessage` with the following fields:
- `message` (string): Message content
- `counter` (int32): Counter value
- `timestamp` (float64): Timestamp value

## Building the Packages

```bash
cd /home/student20/assessments/week3
colcon build
source install/setup.bash
```

## Running the Nodes

### Option 1: Run Publisher and Subscriber Separately

**Terminal 1 - Publisher**:
```bash
ros2 run custom_publisher_package custom_publisher_node.py
```

**Terminal 2 - Subscriber**:
```bash
ros2 run custom_subscriber_package custom_subscriber_node.py
```

### Option 2: Run with Launch Files

**Publisher with custom parameters**:
```bash
ros2 launch custom_publisher_package publisher_launch.py timer_frequency:=2.0 topic_name:=my_topic message_content:="Hello ROS2"
```

**Subscriber with custom parameters**:
```bash
ros2 launch custom_subscriber_package subscriber_launch.py topic_name:=my_topic
```

### Option 3: Run Both with Combined Launch File (Challenge II)

```bash
ros2 launch custom_publisher_package combined_launch.py timer_frequency:=2.0 topic_name:=my_topic message_content:="Hello ROS2"
```

## Launch File Parameters

The launch files support the following parameters:

- **timer_frequency**: Publishing frequency in Hz (default: 1.0)
  ```bash
  ros2 launch custom_publisher_package combined_launch.py timer_frequency:=5.0
  ```

- **topic_name**: Topic name for communication (default: custom_topic)
  ```bash
  ros2 launch custom_publisher_package combined_launch.py topic_name:=my_custom_topic
  ```

- **message_content**: Message content (default: custom_string)
  ```bash
  ros2 launch custom_publisher_package combined_launch.py message_content:="Custom Message"
  ```

## Example Usage

Run the combined launch file with custom parameters:
```bash
ros2 launch custom_publisher_package combined_launch.py \
  timer_frequency:=2.0 \
  topic_name:=test_topic \
  message_content:="Test Message"
```

This will:
1. Start the publisher node publishing to `test_topic` at 2 Hz with content "Test Message"
2. Start the subscriber node listening to `test_topic` and logging received messages

## Verification

To verify the setup is working:

1. **Check running nodes**:
   ```bash
   ros2 node list
   ```

2. **Check topics**:
   ```bash
   ros2 topic list
   ```

3. **Echo topic messages**:
   ```bash
   ros2 topic echo /custom_topic
   ```

4. **Check node information**:
   ```bash
   ros2 node info /custom_publisher_node
   ros2 node info /custom_subscriber_node
   ```

## Challenges Completed

- **Challenge I**: ✅ Created `custom_message_package` with custom message definition
- **Challenge II**: ✅ Created launch files with adjustable parameters (timer frequency, topic names)

## Notes

- All nodes use INFO level logging for visibility
- The publisher publishes at a configurable frequency
- Both nodes support dynamic parameter configuration via launch files
- The custom message package is ready to be used in future exercises
