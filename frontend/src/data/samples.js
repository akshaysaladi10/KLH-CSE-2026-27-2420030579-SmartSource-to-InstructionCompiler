export const SAMPLES = [
  {
    id: "arithmetic",
    title: "1. Arithmetic Basics",
    category: "Basic",
    description: "Simple variable declarations, assignment, and addition.",
    code: `// Example 1: Arithmetic Basics
int a = 10;
int b = 20;
int c;
c = a + b;
print c;
`
  },
  {
    id: "expression",
    title: "2. Expression & Precedence",
    category: "Expressions",
    description: "Complex expression demonstrating arithmetic operator precedence (* before +).",
    code: `// Example 2: Operator Precedence
int a = 10;
int b = 20;
int c;
c = a + b * 2;
print c;
`
  },
  {
    id: "conditional",
    title: "3. Conditional Branching",
    category: "Control Flow",
    description: "If-else statement comparing variables and branching execution.",
    code: `// Example 3: Conditional Branching
int a = 15;
int b = 20;
int c;
if (a > b) {
    c = a;
} else {
    c = b;
}
print c;
`
  },
  {
    id: "loop",
    title: "4. While Loop Accumulator",
    category: "Control Flow",
    description: "While loop computing sum of numbers from 0 to 9.",
    code: `// Example 4: While Loop Accumulator
int i = 0;
int sum = 0;
while (i < 10) {
    sum = sum + i;
    i = i + 1;
}
print sum;
`
  },
  {
    id: "optimization",
    title: "5. Optimization Showcase",
    category: "Optimization",
    description: "Demonstrates Constant Folding (10+20), Constant Propagation, Algebraic Simplification (y+0, z*1), and Dead Code Elimination.",
    code: `// Example 5: Compiler Optimization Showcase
int x = 10 + 20;
int y = x + 0;
int z = y * 1;
int unused = 999;
int result = z * 2;
print result;
`
  },
  {
    id: "factorial",
    title: "6. Factorial Algorithm",
    category: "Algorithms",
    description: "Calculates 5! (factorial of 5) using an iterative while loop.",
    code: `// Example 6: Factorial of 5 (5! = 120)
int n = 5;
int fact = 1;
while (n > 1) {
    fact = fact * n;
    n = n - 1;
}
print fact;
`
  }
];
