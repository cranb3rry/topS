
#include <iostream>
#include <string>


int main()
{
    std::string name1, phone1, address1;
    std::string name2, phone2, address2;
    
    std::cout<<"user1, What is your name? \n";
    std::getline(std::cin, name1);
    std::cout<<"user1, What is your address? \n";
    std::getline(std::cin, address1);
    std::cout<<"user1, What is your phone? \n";
    std::getline(std::cin, phone1);
    
    std::cout<<"user2, What is your name? \n";
    std::getline(std::cin, name2);
    std::cout<<"user2, What is your address? \n";
    std::getline(std::cin, address2);
    std::cout<<"user2, What is your phone? \n";
    std::getline(std::cin, phone2);
    
    std::cout<<"\n"<<name1<<"\n\t\t"<<address1
       <<"\n\t\t"<<phone1<<"\n";

    std::cout<<"\n"<<name2<<"\n\t\t"<<address2
       <<"\n\t\t"<<phone2<<"\n";

    return 0;
}