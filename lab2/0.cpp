#include <assert.h>
#include <stdlib.h>

#include <iostream>

struct Point {
    int x;
    int y;
};

struct Shape {
    enum EType {
        circle,
        square,
        rhombus
    };
    EType type_;
};

struct Circle {
    Shape::EType type_;
    double radius_;
    Point center_;
};

struct Square {
    Shape::EType type_;
    double side_;
    Point center_;
};

struct Rhombus {
    Shape::EType type_;
    double side_;
    double angle_;
    Point center_;
};

void drawSquare(struct Square*) {
    std::cerr << "in drawSquare\n";
}

void drawCircle(struct Circle*) {
    std::cerr << "in drawCircle\n";
}

void drawRhombus(struct Rhombus*) {
    std::cerr << "in drawRhombus\n";
}

void drawShapes(Shape** shapes, int n) {
    for (int i = 0; i < n; ++i) {
        struct Shape* s = shapes[i];
        switch (s->type_) {
            case Shape::square:
                drawSquare((struct Square*)s);
                break;
            case Shape::circle:
                drawCircle((struct Circle*)s);
                break;
            case Shape::rhombus:
                drawRhombus((struct Rhombus*)s);
                break;
            default:
                assert(0);
                exit(0);
        }
    }
}

void moveSquare(struct Square* square, int x, int y) {
    square->center_.x = square->center_.x + x;
    square->center_.y = square->center_.y + y;
    std::cerr << "in moveSquare\n";
}

void moveCircle(struct Circle* circle, int x, int y) {
    circle->center_.x = circle->center_.x + x;
    circle->center_.y = circle->center_.y + y;
    std::cerr << "in moveCircle\n";
}

void moveRhombus(struct Rhombus* rhombus, int x, int y) {
    rhombus->center_.x = rhombus->center_.x + x;
    rhombus->center_.y = rhombus->center_.y + y;
    std::cerr << "in moveRhombus\n";
}

void moveShapes(Shape** shapes, int n, int x, int y) {
    for (int i = 0; i < n; i++) {
        struct Shape* s = shapes[i];
        switch (s->type_) {
            case Shape::square:
                moveSquare((struct Square*)s, x, y);
                break;
            case Shape::circle:
                moveCircle((struct Circle*)s, x, y);
                break;
            case Shape::rhombus:
                moveRhombus((struct Rhombus*)s, x, y);
                break;
            default:
                assert(0);
                exit(0);
        }
    }
}

int main() {
    Shape* shapes[5];
    shapes[0] = (Shape*)new Circle;
    shapes[0]->type_ = Shape::circle;
    shapes[1] = (Shape*)new Square;
    shapes[1]->type_ = Shape::square;
    shapes[2] = (Shape*)new Square;
    shapes[2]->type_ = Shape::square;
    shapes[3] = (Shape*)new Circle;
    shapes[3]->type_ = Shape::circle;
    shapes[4] = (Shape*)new Rhombus;
    shapes[4]->type_ = Shape::rhombus;

    drawShapes(shapes, 5);
    moveShapes(shapes, 5, 5, 5);
}
