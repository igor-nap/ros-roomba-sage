#include "node_example_core.h"

/*--------------------------------------------------------------------
 * main()
 * Main function to set up ROS node.
 *------------------------------------------------------------------*/

int main(int argc, char **argv)
{
  // Set up ROS.
  ros::init(argc, argv, "talker");

  // Declare variables that can be modified by launch file or command line.
  int a;
  int b;
  string message;
  int rate;
  string topic;

  // Initialize node parameters from launch file or command line.
  // Use a private node handle so that multiple instances of the node can
  // be run simultaneously while using different parameters.
  ros::NodeHandle private_node_handle_("~");
  private_node_handle_.param("a", a, int(1));
  private_node_handle_.param("b", b, int(2));
  private_node_handle_.param("message", message, string("hello"));
  private_node_handle_.param("rate", rate, int(40));
  private_node_handle_.param("topic", topic, string("example"));

  // Create a publisher and name the topic.
  ros::Publisher pub_message = n.advertise<node_example::node_example_data>(topic.c_str(), 10);

  // Tell ROS how fast to run this node.
  ros::Rate r(rate);

  // Main loop.
  while (n.ok())
  {
    // Publish the message.
    node_example->publishMessage(&pub_message);

    ros::spinOnce();
    r.sleep();
  }

  return 0;
} // end main()