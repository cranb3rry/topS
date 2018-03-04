/*Goal: practice using stringstream
/*Goal: practice getting string inputs and 
 **converting them to numeric variables using
 **stringstream.
 **
 **Prompt the user for the length of a room. 
 **Then prompt for the width of the room.
 **Print out the area of the room. 
 */

 #include <iostream>
 #include <string>
 #include <sstream>

 int main ()
 {
   std::string length_str;
   std::string width_str;
   float length = 0;
   float width = 0;
   float area = 0;

   std::cout << "Enter a length of the room:\n";
   std::cin >> length_str;
   std::stringstream(length_str) >> length;
   
   std::cout << "Enter a width of the room:\n";
   std::cin >> width_str;
   std::stringstream(width_str) >> width;   
   
   area = width*length;
   std::cout << "area is " << area << "\n";
   return 0;
 }