#include <cstdlib>
#include <iostream>
#include <vector>

using namespace std;

class Point {
   public:
    int x;
    int y;
    Point(){};
    Point(int x, int y) {
        x = x;
        y = y;
    };
};

class Shape {
   public:
    virtual void draw() = 0;
    virtual void move(Point*) = 0;
};

class Circle : public Shape {
   private:
    double side;
    Point center;

   public:
    virtual void draw() {
        cerr << "in drawCircle\n";
    }

    virtual void move(Point* point) {
        center.x = center.x + point->x;
        center.y = center.y + point->y;
        cerr << "in moveCircle\n";
    }
};

class Square : public Shape {
   private:
    double side;
    Point center;

   public:
    virtual void draw() {
        cerr << "in drawSquare\n";
    }

    virtual void move(Point* point) {
        center.x = center.x + point->x;
        center.y = center.y + point->y;
        cerr << "in moveSquare\n";
    }
};

class Rhombus : public Shape {
   private:
    double side;
    Point center;

   public:
    virtual void draw() {
        std::cerr << "in drawRhombus\n";
    }

    virtual void move(Point* point) {
        center.x = center.x + point->x;
        center.y = center.y + point->y;
        std::cerr << "in moveRhombus\n";
    }
};

void drawShapes(const std::vector<Shape*>& shapes) {
    for (auto shape : shapes) {
        shape->draw();
    }
}

void moveShapes(const std::vector<Shape*>& shapes, Point* point) {
    for (auto shape : shapes) {
        shape->move(point);
    }
}

int main() {
    std::vector<Shape*> shapes;
    shapes.push_back(new Circle());
    shapes.push_back(new Square());
    shapes.push_back(new Square);
    shapes.push_back(new Circle());
    shapes.push_back(new Rhombus());

    drawShapes(shapes);
    moveShapes(shapes, new Point(5, 5));
}
