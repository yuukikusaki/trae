---
tags: [408, 数据结构, Ch1, 复杂度, 时间复杂度, 空间复杂度]
aliases: [DS第一章]
---

# Ch1 绪论 —— 复杂度分析是一切的基础

> 🔗 [[DS-MOC-数据结构总览|MOC]] | 下一章：[[DS-Ch2-线性表]] | [[DS-复杂度速查]]

---

## 1.1 时间复杂度：代码运行多久？

### 直接看代码识别复杂度

```c
// ══════════════════════════════════════
// O(1) — 常数阶：不随输入规模变化
// ══════════════════════════════════════
int getFirst(int a[], int n) {
    return a[0];          // 不管 n 多大，只执行 1 次
}

// ══════════════════════════════════════
// O(n) — 线性阶：单层循环
// ══════════════════════════════════════
int sum(int a[], int n) {
    int s = 0;            // 1 次
    for (int i = 0; i < n; i++)
        s += a[i];        // n 次
    return s;             // 1 次
}   // 总 ≈ n → O(n)

// ══════════════════════════════════════
// O(n²) — 平方阶：双层嵌套循环
// ══════════════════════════════════════
void printPairs(int a[], int n) {
    for (int i = 0; i < n; i++)           // n 次
        for (int j = 0; j < n; j++)       // n 次 × n
            printf("%d %d\n", a[i], a[j]); // n² 次
}   // O(n²)

// ══════════════════════════════════════
// O(log n) — 对数阶：每次规模减半
// ══════════════════════════════════════
int binarySearch(int a[], int n, int key) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {            // 每次循环区间减半
        int mid = (lo + hi) / 2;
        if (a[mid] == key) return mid;
        else if (a[mid] < key) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}   // 最多 log₂n 次 → O(log n)

// ══════════════════════════════════════
// O(n log n) — 线形对数阶
// ══════════════════════════════════════
// 典型：归并排序、快速排序（平均）
// 外层 log n 层，每层 O(n) 合并
```

### 408 常考：多层循环的复杂度

```c
// 例1：i 每次 ×2，内层 j 与 i 有关
for (int i = 1; i <= n; i *= 2)       // i: 1,2,4,8,... → log₂n 趟
    for (int j = 1; j <= i; j++)      // 每趟执行 i 次
        sum++;                         // 总次数 = 1+2+4+...+n = 2n-1
// 复杂度：O(n) — 不是 O(n log n)！

// 例2：等差数列型
int x = 0;
while (n >= (x+1)*(x+1))
    x++;
// x² ≈ n → x ≈ √n → O(√n)
```

### 递归复杂度 — 递推公式法

```c
// 递归求阶乘
int fact(int n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);   // T(n) = T(n-1) + O(1)
}                              // → T(n) = O(n)

// 递归求斐波那契（低效写法）
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);  // T(n) = T(n-1) + T(n-2) + O(1)
}                                 // → T(n) = O(2ⁿ)  指数级！
```

| 递推公式 | 结果 | 典型算法 |
|----------|------|----------|
| T(n) = T(n-1) + O(1) | **O(n)** | 阶乘、线性递归 |
| T(n) = T(n/2) + O(1) | **O(log n)** | 二分查找 |
| T(n) = 2T(n/2) + O(n) | **O(n log n)** | 归并排序 |
| T(n) = T(n-1) + O(n) | **O(n²)** | 冒泡/选择排序 |
| T(n) = 2T(n-1) + O(1) | **O(2ⁿ)** | 汉诺塔、递归Fibonacci |

---

## 1.2 空间复杂度：需要多少内存？

```c
// O(1) — 原地算法，只用常数空间
void reverse(int a[], int n) {
    for (int i = 0; i < n/2; i++) {
        int t = a[i];              // 只用了 1 个临时变量
        a[i] = a[n-1-i];
        a[n-1-i] = t;
    }
}

// O(n) — 需要辅助数组
int* copyArray(int a[], int n) {
    int* b = (int*)malloc(n * sizeof(int));  // 分配了 n 大小的空间
    for (int i = 0; i < n; i++) b[i] = a[i];
    return b;
}

// 递归空间复杂度 = 递归深度 × 每层空间
int fact(int n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);   // 递归深度 n，每层 O(1)
}                              // 空间 O(n)（调用栈）
```

---

## 1.3 408 考点速记

| 考点 | 要点 |
|------|------|
| 复杂度比较 | O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!) |
| 加法规则 | T(n) = T₁(n) + T₂(n) = O(max(f(n), g(n))) |
| 乘法规则 | T(n) = T₁(n) × T₂(n) = O(f(n) × g(n)) |
| **只有最高阶起作用** | O(n² + n) = O(n²)；低阶和常数都丢掉 |
| 递归空间 | = **递归深度** × 每层空间 |

### 🔥 易错点

- ❌ `for(i=1; i<=n; i*=2)` 是 O(log₂n)，不是 O(√n)
- ❌ 递归 Fibonacci 时间 O(2ⁿ)，但记忆化后 O(n)
- ❌ 空间复杂度 ≠ 代码中变量个数（递归的调用栈也算）
- ❌ `for(i=0;i<n;i++) for(j=i;j<n;j++)` — 次数 = n+(n-1)+...+1 = n(n+1)/2 → **O(n²)**，不是 O(n log n)

---

## 📝 配套练习：用手算复杂度

以下代码的复杂度分别是多少？

```c
// (1)
int s = 0;
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= i; j *= 2)
        s++;
// 答案：O(n log n)  — 内层 log i 次，外层 n 次

// (2)
int count = 0;
for (int i = 1; i < n; i *= 2)
    count++;
// 答案：O(log n)

// (3) 递归
int func(int n) {
    if (n == 0) return 0;
    return func(n/3) + func(n/3);
}
// 答案：T(n)=2T(n/3)+O(1) — 主定理 → O(n^{log₃2}) ≈ O(n^{0.63})
```

---

> 🔗 下一章：[[DS-Ch2-线性表]] | [[DS-复杂度速查]]
