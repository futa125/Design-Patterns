#include <iostream>
#include <list>
#include <set>
#include <vector>

template <typename Iterator, typename Predicate>
Iterator mymax(Iterator begin, Iterator end, Predicate pred) {
    Iterator max = begin;
    Iterator curr = ++begin;

    while (curr != end) {
        if (pred(*curr, *max)) {
            max = curr;
        }

        curr++;
    }

    return max;
}

int gt_int(const int left, const int right) {
    return left > right;
}

int gt_char(const char left, const char right) {
    return left > right;
}

int gt_str(const char* left, const char* right) {
    return strcmp(left, right) > 0;
}

int gt_string(const std::string left, const std::string right) {
    return left.compare(right) > 0;
}

int main() {
    int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    char arr_char[] = "Suncana strana ulice";
    const char* arr_cstr[] = {
        "Gle",
        "malu",
        "vocku",
        "poslije",
        "kise",
        "Puna",
        "je",
        "kapi",
        "pa",
        "ih",
        "njise",
    };

    std::vector<int> vec_int = std::vector<int>(std::begin(arr_int), std::end(arr_int));
    std::set<char> set_char = std::set<char>(std::begin(arr_char), std::end(arr_char));
    std::list<std::string> list_str = std::list<std::string>(std::begin(arr_cstr), std::end(arr_cstr));

    const int* max_int = mymax(std::begin(arr_int), std::end(arr_int), gt_int);
    const char* max_char = mymax(std::begin(arr_char), std::end(arr_char), gt_char);
    const char** max_cstring = mymax(std::begin(arr_cstr), std::end(arr_cstr), gt_str);

    std::vector<int>::iterator max_vec_int = mymax(vec_int.begin(), vec_int.end(), gt_int);
    std::set<char>::iterator max_set_char = mymax(set_char.begin(), set_char.end(), gt_int);
    std::list<std::string>::iterator max_list_str = mymax(list_str.begin(), list_str.end(), gt_string);

    std::cout << "Max of arr_int: " << *max_int << std::endl;
    std::cout << "Max of arr_char: " << *max_char << std::endl;
    std::cout << "Max of arr_cstr: " << *max_cstring << std::endl;

    std::cout << "Max of vec_int: " << *max_vec_int << std::endl;
    std::cout << "Max of set_char: " << *max_set_char << std::endl;
    std::cout << "Max of list_str: " << *max_list_str << std::endl;
}
