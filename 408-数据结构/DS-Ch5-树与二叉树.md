---
tags: [408, 数据结构, Ch5, 树, 二叉树, BST, 堆, Huffman]
aliases: [DS第五章, 树]
created: 2026-06-04
---

# DS-Ch5 树与二叉树

> [[DS-MOC-数据结构总览|MOC 数据结构总览]] | 上一章：[[DS-Ch4-串]] | 下一章：[[DS-Ch6-图]] | 大题模板：[[DS-大题模板]]

---

## 5.1 树的基本概念

### 5.1.1 定义

树（Tree）是 $n \ (n \ge 0)$ 个结点的有限集。$n=0$ 时称为**空树**。任一非空树满足：
- 有且仅有一个**根**（Root）结点。
- $n>1$ 时，其余结点可分为 $m \ (m>0)$ 个互不相交的有限集，每个集合本身又是一棵树，称为根的**子树**（Subtree）。

### 5.1.2 基本术语

| 术语 | 含义 |
|---|---|
| 结点的**度** | 结点拥有的子树个数 |
| 树的**度** | 树中所有结点的度的最大值 |
| **叶子**（终端结点） | 度为 0 的结点 |
| **分支结点**（非终端结点） | 度 > 0 的结点 |
| **孩子 / 双亲** | 结点的子树的根称为该结点的孩子，该结点是孩子的双亲 |
| **兄弟** | 同一双亲的孩子之间互称兄弟 |
| **祖先 / 子孙** | 从根到某结点路径上的所有结点为其祖先；反之为其子孙 |
| **深度 / 高度** | 根深度为 1（或 0，因教材而异）；树的高度为所有结点层次的最大值 |

### 5.1.3 树的性质

- 树中的结点数 = 所有结点度数之和 + 1
- 度为 $m$ 的树中第 $i$ 层最多有 $m^{i-1}$ 个结点
- 深度为 $h$ 的 $m$ 叉树最多有 $\frac{m^h-1}{m-1}$ 个结点

---

## 5.2 二叉树

### 5.2.1 二叉树的定义与性质

二叉树每个结点最多有两棵子树，且子树有**左右之分**，次序不可颠倒。

**408 考点——二叉树性质：**

| # | 性质 | 408考察频率 |
|---|---|---|
| 1 | 第 $i$ 层最多 $2^{i-1}$ 个结点 | 高 |
| 2 | 深度为 $k$ 的二叉树最多 $2^k-1$ 个结点 | 高 |
| 3 | $n_0 = n_2 + 1$（叶子数 = 度为2的结点数 + 1） | **极高** |
| 4 | $n$ 个结点的完全二叉树深度 $\lfloor \log_2 n \rfloor + 1$ | 高 |
| 5 | 完全二叉树按层编号：$i$ 的左孩子 $2i$，右孩子 $2i+1$，双亲 $\lfloor i/2 \rfloor$ | **极高** |

**n0 = n2 + 1 推导：**
设 $n_0, n_1, n_2$ 分别为度为 0, 1, 2 的结点数。
- 结点总数：$n = n_0 + n_1 + n_2$
- 总度数 = $n_1 + 2n_2$，且总度数 = $n-1$
- $\therefore n_1 + 2n_2 = n_0 + n_1 + n_2 - 1$
- $\therefore n_0 = n_2 + 1$

### 5.2.2 满二叉树 vs 完全二叉树

- **满二叉树**：深度 $k$ 有 $2^k-1$ 个结点，每层都满。
- **完全二叉树**：按层序编号与满二叉树编号一一对应。最后一层可以不满，但结点必须靠左连续。

> **408 技巧**：完全二叉树的叶子只可能出现在最后两层；若某结点只有右孩子无左孩子，必**不**是完全二叉树。

---

## 5.2.3 二叉树的链式存储

二叉链表是 408 最核心的存储方式，每个结点含 `data`、`lchild`、`rchild`。

```c
//========== 二叉树链式存储结构定义 ==========
//==408考点==
typedef char ElemType;   // 假定元素类型为 char

typedef struct BiTNode {
    ElemType data;               // 数据域
    struct BiTNode *lchild;      // 左孩子指针
    struct BiTNode *rchild;      // 右孩子指针
} BiTNode, *BiTree;
```

含有 $n$ 个结点的二叉链表中共有 $n+1$ 个空链域（$2n-(n-1)=n+1$）。这些空链域正是**线索二叉树**的线索存储位置。

### 顺序存储（仅用于完全二叉树场景）

```c
// 顺序存储：数组下标从 1 开始，完全二叉树适用
#define MAXSIZE 100
typedef ElemType SqBiTree[MAXSIZE];  // SqBiTree[0] 通常闲置
// 结点 i 的左孩子：2i, 右孩子：2i+1, 双亲：i/2
```

---

## 5.2.4 递归遍历（先序 / 中序 / 后序）

**408 重中之重**，要求能手写。时间复杂度 $O(n)$，空间复杂度 $O(h)$（递归栈深度，$h$ 为树高）。

```c
//========== 递归遍历三件套 ==========
//==408考点==

// 先序遍历：根 → 左 → 右
void PreOrder(BiTree T) {
    if (T == NULL) return;
    visit(T);               // 访问根结点
    PreOrder(T->lchild);    // 遍历左子树
    PreOrder(T->rchild);    // 遍历右子树
}

// 中序遍历：左 → 根 → 右
void InOrder(BiTree T) {
    if (T == NULL) return;
    InOrder(T->lchild);     // 遍历左子树
    visit(T);               // 访问根结点
    InOrder(T->rchild);     // 遍历右子树
}

// 后序遍历：左 → 右 → 根
void PostOrder(BiTree T) {
    if (T == NULL) return;
    PostOrder(T->lchild);   // 遍历左子树
    PostOrder(T->rchild);   // 遍历右子树
    visit(T);               // 访问根结点
}

// 辅助访问函数
void visit(BiTNode *p) {
    printf("%c ", p->data);
}
```

**408 推导题核心：**
- 先序序列 + 中序序列 → 唯一确定二叉树
- 后序序列 + 中序序列 → 唯一确定二叉树
- 先序序列 + 后序序列 → **不能**唯一确定（无中序无法区分左右）

---

## 5.2.5 非递归遍历（栈实现）

408 大题可能要求**手写非递归遍历**，中序和先序是考察重点。后序非递归较复杂，考察较少。

### 先序非递归

```c
//========== 先序非递归遍历（栈） ==========
//==408考点==
#include <stdbool.h>

#define MAX_STACK 100

void PreOrder_NonRecursive(BiTree T) {
    BiTNode *stack[MAX_STACK];
    int top = -1;
    BiTNode *p = T;

    while (p != NULL || top != -1) {
        if (p != NULL) {
            visit(p);                    // 先访问根
            stack[++top] = p;            // 根入栈（用于后面找右子树）
            p = p->lchild;               // 走向左子树
        } else {
            p = stack[top--];            // 弹出
            p = p->rchild;               // 走向右子树
        }
    }
}
```

### 中序非递归（408 最爱考）

```c
//========== 中序非递归遍历（栈） ==========
//==408考点==  —— 大题手写高频

void InOrder_NonRecursive(BiTree T) {
    BiTNode *stack[MAX_STACK];
    int top = -1;
    BiTNode *p = T;

    while (p != NULL || top != -1) {
        if (p != NULL) {
            stack[++top] = p;            // 根入栈
            p = p->lchild;               // 一路向左走到底
        } else {
            p = stack[top--];            // 弹出栈顶（最左结点）
            visit(p);                    // 访问之
            p = p->rchild;               // 转向右子树
        }
    }
}
```

### 后序非递归（了解即可）

```c
//========== 后序非递归遍历 ==========
// 使用双栈法或标记法，408 考频较低

void PostOrder_NonRecursive(BiTree T) {
    BiTNode *stack1[MAX_STACK];      // 模拟"根→右→左"
    BiTNode *stack2[MAX_STACK];      // 反转得到"左→右→根"
    int top1 = -1, top2 = -1;
    BiTNode *p;

    if (T == NULL) return;

    stack1[++top1] = T;
    while (top1 != -1) {
        p = stack1[top1--];
        stack2[++top2] = p;          // 进入 stack2
        if (p->lchild) stack1[++top1] = p->lchild;
        if (p->rchild) stack1[++top1] = p->rchild;
    }

    while (top2 != -1) {
        p = stack2[top2--];
        visit(p);
    }
}
```

---

## 5.2.6 层序遍历（队列实现）

```c
//========== 层序遍历（队列） ==========
//==408考点==

#define MAX_QUEUE 100

typedef struct {
    BiTNode *data[MAX_QUEUE];
    int front;    // 队头指针
    int rear;     // 队尾指针
} Queue;

void InitQueue(Queue *Q) {
    Q->front = Q->rear = 0;
}

bool EnQueue(Queue *Q, BiTNode *node) {
    if ((Q->rear + 1) % MAX_QUEUE == Q->front) return false;  // 队满
    Q->data[Q->rear] = node;
    Q->rear = (Q->rear + 1) % MAX_QUEUE;
    return true;
}

bool DeQueue(Queue *Q, BiTNode **node) {
    if (Q->front == Q->rear) return false;                    // 队空
    *node = Q->data[Q->front];
    Q->front = (Q->front + 1) % MAX_QUEUE;
    return true;
}

bool QueueEmpty(Queue *Q) {
    return Q->front == Q->rear;
}

void LevelOrder(BiTree T) {
    Queue Q;
    InitQueue(&Q);
    BiTNode *p;

    if (T == NULL) return;

    EnQueue(&Q, T);
    while (!QueueEmpty(&Q)) {
        DeQueue(&Q, &p);
        visit(p);
        if (p->lchild != NULL) EnQueue(&Q, p->lchild);
        if (p->rchild != NULL) EnQueue(&Q, p->rchild);
    }
}
```

---

## 5.2.7 求树高 / 结点数 / 叶子数

```c
//========== 二叉树属性计算（递归） ==========
//==408考点==

// (1) 求树的高度
int GetHeight(BiTree T) {
    if (T == NULL) return 0;
    int LH = GetHeight(T->lchild);
    int RH = GetHeight(T->rchild);
    return (LH > RH ? LH : RH) + 1;
}

// (2) 求结点总数
int GetNodeCount(BiTree T) {
    if (T == NULL) return 0;
    return GetNodeCount(T->lchild) + GetNodeCount(T->rchild) + 1;
}

// (3) 求叶子结点数
int GetLeafCount(BiTree T) {
    if (T == NULL) return 0;
    if (T->lchild == NULL && T->rchild == NULL) return 1;
    return GetLeafCount(T->lchild) + GetLeafCount(T->rchild);
}

// (4) 求第 k 层结点数（根为第 1 层）
int GetKLevelCount(BiTree T, int k) {
    if (T == NULL || k < 1) return 0;
    if (k == 1) return 1;
    return GetKLevelCount(T->lchild, k - 1)
         + GetKLevelCount(T->rchild, k - 1);
}
```

---

## 5.3 线索二叉树

### 5.3.1 为什么需要线索二叉树

$n$ 个结点的二叉链表有 $n+1$ 个空链域。将这些空链域用来存储**前驱**和**后继**信息，即为线索。线索化后遍历二叉树不需要栈/递归，空间 $O(1)$。

### 5.3.2 结构定义

```c
//========== 线索二叉树结构 ==========
//==408考点==

// 线索标志位：Link(0) 表示指向孩子, Thread(1) 表示指向前驱/后继
typedef enum { Link, Thread } PointerTag;

typedef struct ThreadNode {
    ElemType data;
    struct ThreadNode *lchild;
    struct ThreadNode *rchild;
    PointerTag ltag;     // 左标志
    PointerTag rtag;     // 右标志
} ThreadNode, *ThreadTree;
```

### 5.3.3 中序线索化

```c
//========== 中序线索化 ==========
//==408考点==

// 全局变量：始终指向前一个访问的结点
ThreadNode *pre = NULL;

void InThread(ThreadNode *p) {
    if (p == NULL) return;

    InThread(p->lchild);          // 线索化左子树

    // --- 线索化当前结点 ---
    if (p->lchild == NULL) {      // 左子树为空，建立前驱线索
        p->ltag = Thread;
        p->lchild = pre;
    }

    if (pre != NULL && pre->rchild == NULL) {
        pre->rtag = Thread;       // 建立前驱的后继线索
        pre->rchild = p;
    }

    pre = p;                      // 保持 pre 指向 p 的前驱
    // --- 线索化完成 ---

    InThread(p->rchild);          // 线索化右子树
}

void CreateInThread(ThreadTree T) {
    pre = NULL;
    if (T != NULL) {
        InThread(T);
        // 处理最后一个结点
        if (pre->rchild == NULL) {
            pre->rtag = Thread;
        }
    }
}
```

### 5.3.4 中序线索二叉树中找前驱 / 后继

```c
//========== 中序线索二叉树：找前驱与后继 ==========
//==408考点==

// 找中序后继
// 若 rtag==Thread, rchild 即为后继；否则后继是右子树的最左下结点
ThreadNode* InOrderSuccessor(ThreadNode *p) {
    if (p->rtag == Thread) return p->rchild;

    // 否则是右子树的最左下结点
    ThreadNode *q = p->rchild;
    while (q->ltag == Link) {
        q = q->lchild;
    }
    return q;
}

// 找中序前驱
// 若 ltag==Thread, lchild 即为前驱；否则前驱是左子树的最右下结点
ThreadNode* InOrderPredecessor(ThreadNode *p) {
    if (p->ltag == Thread) return p->lchild;

    ThreadNode *q = p->lchild;
    while (q->rtag == Link) {
        q = q->rchild;
    }
    return q;
}

// 中序线索二叉树的中序遍历（非递归、无栈）
void InOrder_Threaded(ThreadTree T) {
    ThreadNode *p = T;
    // 找到中序遍历的第一个结点（最左下结点）
    while (p->ltag == Link) {
        p = p->lchild;
    }
    // 依次输出后继
    while (p != NULL) {
        printf("%c ", p->data);
        p = InOrderSuccessor(p);
    }
}
```

---

## 5.4 树与二叉树的转换

### 5.4.1 孩子兄弟表示法（左孩子右兄弟）

这是树 → 二叉树转换的标准方法，也是 408 树存储的默认方式。

```c
//========== 孩子兄弟表示法 ==========
//==408考点==

typedef struct CSNode {
    ElemType data;
    struct CSNode *firstchild;   // 指向第一个孩子（相当于二叉树的 lchild）
    struct CSNode *nextsibling;  // 指向下一个兄弟（相当于二叉树的 rchild）
} CSNode, *CSTree;
```

### 5.4.2 [转换规则](https://blog.csdn.net/xiangjunyes/article/details/106996411)

| 操作       | 规则                                          |
| -------- | ------------------------------------------- |
| 树 → 二叉树  | 左孩子右兄弟：每个结点的**第一个孩子**作为其左孩子，**下一个兄弟**作为其右孩子 |
| 二叉树 → 树  | 逆操作：左孩子变成第一个孩子，右孩子变成下一个兄弟                   |
| 森林 → 二叉树 | 各树的根视作兄弟，用右指针相连                             |
| 二叉树 → 森林 | 逆操作：沿根结点的右链拆开                               |

**408 结论：**
- 树转换成二叉树后，根结点无右子树
- 二叉树无右子树 ↔ 对应的树只有一棵（非森林）
- 树的中序遍历 = 对应二叉树的中序遍历（孩子兄弟表示法下）

---

## 5.5 二叉排序树 BST

### 5.5.1 定义

二叉排序树（Binary Search Tree）是一棵空树，或满足：
- 左子树所有结点值 < 根结点值
- 右子树所有结点值 > 根结点值
- 左右子树也各是 BST

**中序遍历 BST 得到递增有序序列。**

### 5.5.2 查找

```c
//========== BST 查找（递归 & 非递归） ==========
//==408考点==

typedef int KeyType;  // 为简化，假定 key 为 int

typedef struct BSTNode {
    KeyType key;
    struct BSTNode *lchild;
    struct BSTNode *rchild;
} BSTNode, *BSTree;

// 递归查找
BSTNode* BST_Search_Recur(BSTree T, KeyType key) {
    if (T == NULL || T->key == key) return T;
    if (key < T->key)
        return BST_Search_Recur(T->lchild, key);
    else
        return BST_Search_Recur(T->rchild, key);
}

// 非递归查找（408 大题推荐使用，效率更高）
BSTNode* BST_Search(BSTree T, KeyType key) {
    while (T != NULL && T->key != key) {
        if (key < T->key)
            T = T->lchild;
        else
            T = T->rchild;
    }
    return T;
}
```

### 5.5.3 插入

```c
//========== BST 插入 ==========
//==408考点==

// 返回插入后树的根（插入操作不会改变已有结点关系）
bool BST_Insert(BSTree *T, KeyType key) {
    if (*T == NULL) {
        // 找到插入位置
        BSTNode *s = (BSTNode *)malloc(sizeof(BSTNode));
        s->key = key;
        s->lchild = s->rchild = NULL;
        *T = s;
        return true;
    }
    if (key == (*T)->key)
        return false;              // BST 中不允许重复 key（也可约定放右子树）
    else if (key < (*T)->key)
        return BST_Insert(&((*T)->lchild), key);
    else
        return BST_Insert(&((*T)->rchild), key);
}
```

### 5.5.4 删除（三种情况）

```c
//========== BST 删除 —— 三种情况 ==========
//==408考点== 大题极高频

// 情况1：被删结点是叶子 → 直接删除
// 情况2：被删结点只有左子树或只有右子树 → 用子树替代
// 情况3：被删结点有左右子树 → 用中序后继（或前驱）替代

bool BST_Delete(BSTree *T, KeyType key) {
    if (*T == NULL) return false;  // 未找到

    // --- 定位要删除的结点 ---
    if (key < (*T)->key)
        return BST_Delete(&((*T)->lchild), key);
    else if (key > (*T)->key)
        return BST_Delete(&((*T)->rchild), key);
    else {
        // 找到了要删除的结点 *T
        BSTNode *del = *T;

        // 情况1 & 情况2：单分支或叶子
        if ((*T)->lchild == NULL) {
            *T = (*T)->rchild;
            free(del);
        }
        else if ((*T)->rchild == NULL) {
            *T = (*T)->lchild;
            free(del);
        }
        // 情况3：左右子树均存在
        else {
            // 找中序后继（右子树的最左下结点）
            BSTNode *succ_parent = *T;
            BSTNode *succ = (*T)->rchild;
            while (succ->lchild != NULL) {
                succ_parent = succ;
                succ = succ->lchild;
            }

            // 用后继的值覆盖被删结点
            (*T)->key = succ->key;

            // 删除后继结点（它一定没有左孩子，可能是情况1或2）
            if (succ_parent == *T)
                succ_parent->rchild = succ->rchild;  // 后继就是右孩子
            else
                succ_parent->lchild = succ->rchild;  // 后继是左孩子

            free(succ);
        }
        return true;
    }
}
```

> **408 细节**：情况3 中找**中序前驱**替换同样正确。选前驱时，将左子树最右下结点的值覆盖过来即可。

---

## 5.6 平衡二叉树 AVL

### 5.6.1 定义与平衡因子

AVL 树是一棵 BST，且任意结点的**左右子树高度差不超过 1**。

$$\text{平衡因子 } BF = \text{左子树高} - \text{右子树高} \in \{-1, 0, 1\}$$

```c
//========== AVL 树结点定义 ==========
//==408考点==

typedef struct AVLNode {
    KeyType key;
    int bf;                      // 平衡因子 (balance factor)
    struct AVLNode *lchild;
    struct AVLNode *rchild;
} AVLNode, *AVLTree;
```

### 5.6.2 四种旋转

插入导致不平衡时，沿插入路径找到**第一个 $|BF| > 1$ 的祖先**（最小不平衡子树的根），对其旋转。

```c
//========== AVL 四种旋转 ==========
//==408考点==  大题手写高频

// 获取高度
int AVL_Height(AVLNode *p) {
    if (p == NULL) return 0;
    int lh = AVL_Height(p->lchild);
    int rh = AVL_Height(p->rchild);
    return (lh > rh ? lh : rh) + 1;
}

// 更新平衡因子
void AVL_UpdateBF(AVLNode *p) {
    if (p == NULL) return;
    p->bf = AVL_Height(p->lchild) - AVL_Height(p->rchild);
}

//========== LL 旋转（右单旋）==========
// 插入位置：LL（在最小不平衡子树根的左子树的左子树上插入）
//          A (BF=2)
//         / \
//    (1) B   AR     →    旋转后 B 成为新根
//       / \
//      C   BR
//     /
//   (new)
AVLNode* AVL_RotateLL(AVLNode *A) {
    AVLNode *B = A->lchild;
    A->lchild = B->rchild;     // B 的右子树给 A 做左子树
    B->rchild = A;             // A 变成 B 的右子树
    AVL_UpdateBF(A);
    AVL_UpdateBF(B);
    return B;                  // B 成为新根
}

//========== RR 旋转（左单旋）==========
// 插入位置：RR（在右子树的右子树上插入）
//    A (BF=-2)
//   / \
//  AL  B (-1)       →    旋转后 B 成为新根
//     / \
//    BL  C
//         \
//        (new)
AVLNode* AVL_RotateRR(AVLNode *A) {
    AVLNode *B = A->rchild;
    A->rchild = B->lchild;     // B 的左子树给 A 做右子树
    B->lchild = A;             // A 变成 B 的左子树
    AVL_UpdateBF(A);
    AVL_UpdateBF(B);
    return B;                  // B 成为新根
}

//========== LR 旋转（先左后右双旋）==========
// 插入位置：LR（在左子树的右子树上插入）
//       A (BF=2)
//      / \
// (-1)B   AR
//    / \
//   BL  C
//      / \
//     CL CR    ← new 可能插在 CL 或 CR 下
AVLNode* AVL_RotateLR(AVLNode *A) {
    A->lchild = AVL_RotateRR(A->lchild);  // 先对 B 左旋
    return AVL_RotateLL(A);               // 再对 A 右旋
}

//========== RL 旋转（先右后左双旋）==========
// 插入位置：RL（在右子树的左子树上插入）
//    A (BF=-2)
//   / \
//  AL  B (1)
//     / \
//    C   BR
//   / \
//  CL CR     ← new 可能插在 CL 或 CR 下
AVLNode* AVL_RotateRL(AVLNode *A) {
    A->rchild = AVL_RotateLL(A->rchild);  // 先对 B 右旋
    return AVL_RotateRR(A);               // 再对 A 左旋
}
```

### 5.6.3 AVL 插入（完整代码）

```c
//========== AVL 插入（含自动平衡调整） ==========
//==408考点==

AVLNode* AVL_Insert(AVLNode *T, KeyType key, bool *taller) {
    // 插入新结点
    if (T == NULL) {
        T = (AVLNode *)malloc(sizeof(AVLNode));
        T->key = key;
        T->lchild = T->rchild = NULL;
        T->bf = 0;
        *taller = true;        // 树增高了
        return T;
    }

    if (key == T->key) {
        *taller = false;       // 不插入重复值
        return T;
    }

    if (key < T->key) {
        // 在左子树中递归插入
        T->lchild = AVL_Insert(T->lchild, key, taller);
        if (*taller) {         // 左子树增高
            switch (T->bf) {
                case 1:        // 原来左高，插入后更高 → 失衡
                    if (key < T->lchild->key)   // LL
                        T = AVL_RotateLL(T);
                    else                         // LR
                        T = AVL_RotateLR(T);
                    *taller = false;
                    break;
                case 0:        // 原来平衡
                    T->bf = 1;
                    *taller = true;
                    break;
                case -1:       // 原来右高，插入后平衡
                    T->bf = 0;
                    *taller = false;
                    break;
            }
        }
    } else {
        // 在右子树中递归插入
        T->rchild = AVL_Insert(T->rchild, key, taller);
        if (*taller) {         // 右子树增高
            switch (T->bf) {
                case 1:        // 原来左高，插入后平衡
                    T->bf = 0;
                    *taller = false;
                    break;
                case 0:        // 原来平衡
                    T->bf = -1;
                    *taller = true;
                    break;
                case -1:       // 原来右高，插入后更高 → 失衡
                    if (key > T->rchild->key)   // RR
                        T = AVL_RotateRR(T);
                    else                         // RL
                        T = AVL_RotateRL(T);
                    *taller = false;
                    break;
            }
        }
    }
    return T;
}
```

### 5.6.4 旋转判定速查

| 插入场景 | 失衡结点 BF | 插入侧/子树 | 旋转 |
|---|---|---|---|
| 在左子树的左子树上插入 | +2 | LL | 右单旋（LL） |
| 在右子树的右子树上插入 | -2 | RR | 左单旋（RR） |
| 在左子树的右子树上插入 | +2 | LR | 先左后右（LR） |
| 在右子树的左子树上插入 | -2 | RL | 先右后左（RL） |

> **408 口诀**：失衡看符号，正 L 负 R；插入与失衡同侧则单旋，异侧则双旋。

---

## 5.7 堆

### 5.7.1 定义

堆是一棵**完全二叉树**，满足：
- **大根堆**：$L(i) \ge L(2i)$ 且 $L(i) \ge L(2i+1)$，即根 $\ge$ 左右孩子
- **小根堆**：$L(i) \le L(2i)$ 且 $L(i) \le L(2i+1)$

通常用**数组**（下标从 1 开始）存储。

### 5.7.2 堆的基本操作

```c
//========== 大根堆完整实现 ==========
//==408考点==

// 数组下标从 1 开始，heap[0] 闲置（或作哨兵）
#define MAX_HEAP 100

typedef struct {
    int data[MAX_HEAP];
    int size;         // 当前堆中元素个数
} MaxHeap;

// 交换
void swap(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

//========== 上滤（Percolate Up）—— 插入时使用 ==========
// 新结点放在末尾，向上比较调整
void Heap_Up(MaxHeap *H, int k) {
    // k 为当前需要上滤的结点下标
    while (k > 1 && H->data[k] > H->data[k / 2]) {
        swap(&H->data[k], &H->data[k / 2]);
        k = k / 2;
    }
}

//========== 下滤（Percolate Down）—— 删除和建堆时使用 ==========
void Heap_Down(MaxHeap *H, int k) {
    // k 为当前需要下滤的结点下标
    while (2 * k <= H->size) {           // 有左孩子
        int j = 2 * k;                   // j 指向左孩子
        if (j < H->size && H->data[j] < H->data[j + 1])
            j++;                         // j 指向左右孩子中较大者
        if (H->data[k] >= H->data[j])
            break;                       // 已满足堆性质
        swap(&H->data[k], &H->data[j]);
        k = j;
    }
}

//========== 插入 O(log n) ==========
bool Heap_Insert(MaxHeap *H, int x) {
    if (H->size >= MAX_HEAP - 1) return false;  // 堆满
    H->data[++H->size] = x;            // 放在末尾
    Heap_Up(H, H->size);               // 上滤调整
    return true;
}

//========== 删除堆顶 O(log n) ==========
bool Heap_DeleteMax(MaxHeap *H, int *max) {
    if (H->size == 0) return false;    // 堆空
    *max = H->data[1];                 // 堆顶即最大元素
    H->data[1] = H->data[H->size--];   // 末尾元素移到堆顶
    Heap_Down(H, 1);                   // 下滤调整
    return true;
}

//========== 建堆 O(n) ==========
// 从最后一个非叶结点 ⌊n/2⌋ 开始向前逐个下滤
void BuildHeap(MaxHeap *H, int arr[], int n) {
    H->size = n;
    for (int i = 1; i <= n; i++) {
        H->data[i] = arr[i - 1];       // arr 是 0-indexed
    }
    for (int i = n / 2; i >= 1; i--) {
        Heap_Down(H, i);
    }
}
```

> **建堆为何是 $O(n)$？** 第 $h$ 层有 $2^{h-1}$ 个结点，每个最多下滤 $(\text{树高}-h)$ 次，累加得 $O(n)$。虽然是粗略下界分析，但 408 记住结论即可。

### 5.7.3 堆排序思想

```c
//========== 堆排序 O(n log n) ==========
//==408考点==

void HeapSort(int arr[], int n) {
    MaxHeap H;
    BuildHeap(&H, arr, n);             // 建大根堆 O(n)

    // 逐次将堆顶（最大值）与末尾交换，然后缩小堆并下滤
    for (int i = H.size; i > 1; i--) {
        swap(&H.data[1], &H.data[i]);   // 堆顶（max）放到末尾
        H.size--;                       // 堆规模 -1
        Heap_Down(&H, 1);               // 从根下滤 O(log n)
    }

    // 此时 H.data[1..n] 即为升序排列（原大根堆变升序）
    for (int i = 0; i < n; i++) {
        arr[i] = H.data[i + 1];
    }
}
```

> **408 关键**：建大根堆 → 升序；建小根堆 → 降序。堆排序不稳定。

---

## 5.8 哈夫曼树与哈夫曼编码

### 5.8.1 定义

- **路径长度**：从根到某结点路径上的边数。
- **带权路径长度 WPL**：$\displaystyle WPL = \sum_{i=1}^{n} w_i \cdot l_i$，$l_i$ 为第 $i$ 个叶子结点的路径长度。
- **哈夫曼树**（最优二叉树）：在 $n$ 个带权叶子构成的所有二叉树中，**WPL 最小**的二叉树。

### 5.8.2 哈夫曼树性质

- $n$ 个叶子结点的哈夫曼树共有 **$2n-1$** 个结点
- 哈夫曼树中**不存在度为 1 的结点**（$n_1 = 0$）
- 哈夫曼树不唯一，但**WPL 唯一且最小**

### 5.8.3 构造算法

```c
//========== 哈夫曼树构造 ==========
//==408考点==

// 哈夫曼树结点
typedef struct {
    int weight;            // 权值
    int parent;            // 双亲下标
    int lchild;            // 左孩子下标
    int rchild;            // 右孩子下标
} HTNode;

// n 个叶子结点 → 哈夫曼树共 2n-1 个结点
// 使用顺序存储，下标 1..(2n-1)
void CreateHuffmanTree(HTNode HT[], int w[], int n) {
    int m = 2 * n - 1;     // 总结点数

    // 初始化 1..m
    for (int i = 1; i <= m; i++) {
        HT[i].parent = HT[i].lchild = HT[i].rchild = 0;
        HT[i].weight = (i <= n) ? w[i - 1] : 0;
    }

    // 构造 n-1 个内部结点
    for (int i = n + 1; i <= m; i++) {
        // 选出两个权值最小且 parent == 0 的结点
        int min1 = INT_MAX, min2 = INT_MAX;
        int s1 = 0, s2 = 0;

        for (int j = 1; j < i; j++) {
            if (HT[j].parent == 0) {
                if (HT[j].weight < min1) {
                    min2 = min1; s2 = s1;
                    min1 = HT[j].weight; s1 = j;
                } else if (HT[j].weight < min2) {
                    min2 = HT[j].weight; s2 = j;
                }
            }
        }

        HT[s1].parent = HT[s2].parent = i;
        HT[i].lchild = s1;
        HT[i].rchild = s2;
        HT[i].weight = HT[s1].weight + HT[s2].weight;
    }
}
```

### 5.8.4 哈夫曼编码

```c
//========== 哈夫曼编码 ==========
//==408考点==

// 从叶子向上回溯到根，逆序得到编码
void HuffmanCoding(HTNode HT[], int n, char *HC[]) {
    // HC 存储每个字符的哈夫曼编码（字符串）
    char *code = (char *)malloc(n * sizeof(char));  // 临时存储
    code[n - 1] = '\0';                              // 编码结束符

    for (int i = 1; i <= n; i++) {
        int start = n - 1;
        int c = i;                     // 当前结点（叶子）
        int f = HT[i].parent;          // 双亲

        while (f != 0) {
            if (HT[f].lchild == c)
                code[--start] = '0';   // 左孩子 → 0
            else
                code[--start] = '1';   // 右孩子 → 1
            c = f;
            f = HT[f].parent;
        }

        // 将编码复制到 HC[i-1]
        HC[i - 1] = (char *)malloc((n - start) * sizeof(char));
        strcpy(HC[i - 1], &code[start]);
    }
    free(code);
}
```

**哈夫曼编码性质：**
- **前缀编码**：任一字符编码不是另一字符编码的前缀
- **最优前缀编码**：WPL 最小
- 编码不等长，字符频率越高编码越短

### 5.8.5 WPL 手工计算方法

> **408 快速求 WPL**：构造出哈夫曼树后，WPL = 所有**非根非叶结点**（即所有内部合并结点）的权值之和。

---

## 5.9 复杂度对比表

| 操作 | 二叉树（一般） | BST（一般） | BST（最坏） | AVL | 堆 |
|---|---|---|---|---|---|
| 查找 | $O(n)$ | $O(h)$ | $O(n)$ | $O(\log n)$ | $O(n)$ |
| 插入 | — | $O(h)$ | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| 删除 | — | $O(h)$ | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| 找最大 | $O(n)$ | $O(h)$ | $O(n)$ | $O(\log n)$ | $O(1)$ |
| 找最小 | $O(n)$ | $O(h)$ | $O(n)$ | $O(\log n)$ | $O(1)$ |
| 建树/堆 | — | $O(n \log n)$ | $O(n^2)$ | $O(n \log n)$ | $O(n)$ |
| 遍历 | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |

> 注：$h$ 为树高。BST 的 $h$ 在最好情况（平衡）下为 $O(\log n)$，最坏（单链）为 $O(n)$。

---

## 5.10 408 易错点总结

| 编号 | 易错点 | 说明 |
|---|---|---|
| 1 | **二叉树左右次序固定** | 交换左右子树后是一棵**不同的二叉树**，切记 |
| 2 | **度为2的树 ≠ 二叉树** | 度为2的树允许只有一个孩子且不区分左右；二叉树区分左右且允许最大度=2，可以只有右孩子 |
| 3 | **n0 = n2 + 1** | 对任何非空二叉树均成立，不限于完全/满二叉树 |
| 4 | **完全二叉树编号** | 下标从 1 开始：左=2i，右=2i+1；若从 0 开始：左=2i+1，右=2i+2 |
| 5 | **完全二叉树的判定** | 某结点只有右孩子无左孩子 → 必非完全二叉树 |
| 6 | **BST 中序遍历有序** | BST ⇔ 中序有序，408 常结合排序考查 |
| 7 | **BST 删除三种情况** | 左右均有时可选择中序后继或前驱替代，都正确 |
| 8 | **AVL 旋转后 BF 更新** | 必须重新计算高度再更新 BF，不能靠推导/猜测 |
| 9 | **堆是逻辑结构** | 堆本身不是物理存储结构，一般用数组作为物理存储 |
| 10 | **建堆 O(n) 不是 O(n log n)** | 408 常设陷阱：建堆是 O(n)，堆排序才是 O(n log n) |
| 11 | **堆排序不稳定** | 因为交换时可能改变相同元素的相对次序 |
| 12 | **哈夫曼树 n1 = 0** | 哈夫曼树中不存在度为 1 的结点，利用此性质可快速计算总结点数 |
| 13 | **哈夫曼编码是前缀编码** | 以此保证解码无歧义 |
| 14 | **先序+后序不能唯一确定二叉树** | 只有「先序+中序」或「后序+中序」可以 |
| 15 | **线索二叉树的 ltag/rtag** | Link=0 表示孩子，Thread=1 表示线索；混淆是常见失分点 |
| 16 | **叶子结点在二叉链表中** | 其 lchild 和 rchild 均为 NULL，即两个空链域 |

---

## 5.11 本章公式速查

- 结点总数与度：$n = n_0 + n_1 + n_2$，$\sum \text{度} = n_1 + 2n_2 = n-1$
- 叶子与度为2结点：$n_0 = n_2 + 1$
- 二叉链表空指针域：$n+1$ 个
- 完全二叉树高度：$\lfloor \log_2 n \rfloor + 1$（$n$ 个结点）
- 哈夫曼树总结点数：$2n-1$（$n$ 个叶子）
- 哈夫曼树 $n_1 = 0$，叶子数 = 内部结点数 + 1

---

> 上一章：[[DS-Ch4-串]] | 下一章：[[DS-Ch6-图]] | 大题模板：[[DS-大题模板]] | [[DS-MOC-数据结构总览|MOC 数据结构总览]]

---

## 🎯 力扣推荐（二叉树核心必刷）

> 💡 你有编程基础，二叉树的题是**力扣上题量最大**的类别。以下按"必做→进阶"分梯队推荐。

### 第1梯队：遍历与基础（必做，每题掌握递归+非递归两种写法）

| 题目 | 难度 | 推荐理由 | 408考点关联 |
|------|------|----------|------------|
| [144. 二叉树的前序遍历](https://leetcode.cn/problems/binary-tree-preorder-traversal/) | 简单 | 递归+非递归 | 408遍历基础 |
| [94. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/) | 简单 | ⭐ **中序非递归=408大题最爱** | 与笔记中 InOrder_NonRecursive 完全一致 |
| [145. 二叉树的后序遍历](https://leetcode.cn/problems/binary-tree-postorder-traversal/) | 简单 | 双栈法/标记法 | 后序非递归（笔记已覆盖） |
| [102. 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/) | 中等 | 队列实现 | 408层序遍历标准模板 |
| [104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) | 简单 | 递归经典 | 与笔记 GetHeight 完全一致 |
| [226. 翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/) | 简单 | 递归/层序都可以 | 408"二叉树左右子树交换" |

### 第2梯队：BST与性质（408大题方向）

| 题目 | 难度 | 推荐理由 | 408考点关联 |
|------|------|----------|------------|
| [98. 验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/) | 中等 | **中序遍历判断递增** | ⭐ BST定义的核心应用 |
| [700. 二叉搜索树中的搜索](https://leetcode.cn/problems/search-in-a-binary-search-tree/) | 简单 | BST查找 | 与笔记 BST_Search 一致 |
| [701. 二叉搜索树中的插入操作](https://leetcode.cn/problems/insert-into-a-binary-search-tree/) | 中等 | BST插入 | 与笔记 BST_Insert 一致 |
| [450. 删除二叉搜索树中的节点](https://leetcode.cn/problems/delete-node-in-a-bst/) | 中等 | 三种情况 | ⭐ **BST删除三种情况=408大题极高频** |
| [108. 将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/) | 简单 | 递归构建BST | 408中"有序序列→BST"的构造 |
| [235. 二叉搜索树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 中等 | BST特性 | 利用BST性质O(h)解决 |
| [230. 二叉搜索树中第K小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/) | 中等 | 中序遍历 | 408"BST中序有序"的应用 |

### 第3梯队：综合与构造（拔高）

| 题目 | 难度 | 推荐理由 | 408考点关联 |
|------|------|----------|------------|
| [105. 从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | 中等 | ⭐ **递归构造** | 408**先序+中序→唯一确定二叉树** |
| [106. 从中序与后序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) | 中等 | 同上 | 408**后序+中序→唯一确定二叉树** |
| [236. 二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/) | 中等 | 递归后序遍历 | 408中二叉树的高级递归 |
| [114. 二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/) | 中等 | 递归/迭代 | 树与链表的结合题 |
| [199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/) | 中等 | 层序变体 | 408层序的灵活运用 |
| [110. 平衡二叉树](https://leetcode.cn/problems/balanced-binary-tree/) | 简单 | 后序判断 | 与AVL的定义思想一致 |

### 刷题路线（针对有编程基础者）

```
阶段1（3天）→ 遍历六题：144, 94, 145, 102, 104, 226
          要求：每种遍历都要能手写递归+非递归两种版本

阶段2（3天）→ BST六题：98, 700, 701, 450, 108, 230
          要求：BST删除(bucket)三种情况要能流畅写出

阶段3（2天）→ 构造三题：105, 106, 236
          要求：自己推理出递归逻辑，而非背代码
```

---

## 🔥 408考点补充：二叉树的推导

### 先序+中序推导二叉树（手算模板）

```
先序: 根 | 左子树 | 右子树
中序: 左子树 | 根 | 右子树

步骤：
1. 先序第一个元素是根
2. 在中序中找到根，左边是左子树，右边是右子树
3. 递归处理左右子树
```

### 后序+中序推导二叉树

```
后序: 左子树 | 右子树 | 根
中序: 左子树 | 根 | 右子树

步骤：
1. 后序最后一个元素是根
2. 在中序中找到根，左边是左子树，右边是右子树
3. 递归处理左右子树
```

---

## 📖 教材补充：二叉树的顺序存储与链式存储

二叉树的顺序存储**仅适用于完全二叉树**。对于一般二叉树，需要在数组中用"虚结点"补全，造成空间浪费。

| 存储方式 | 适用场景 | 优点 | 缺点 |
|----------|----------|------|------|
| 顺序存储 | 完全二叉树/堆 | 随机存取，无指针开销 | 一般二叉树空间浪费大 |
| 链式存储（二叉链表） | 一般二叉树 | 空间利用率高 | n个结点有n+1个空链域 |
| 三叉链表 | 需要找双亲的场景 | 可快速找双亲 | 额外指针开销更大 |

---

## 🔥 教材补充：完全二叉树的重要性质

对于按层序编号的完全二叉树（根从1开始），结点 i 的：
- 左孩子：2i（若2i ≤ n）
- 右孩子：2i+1（若2i+1 ≤ n）
- 双亲：⌊i/2⌋
- 判断是否为叶子：i > ⌊n/2⌋

> **408常见陷阱**：完全二叉树中度为1的结点**最多1个**，且该结点**只有左孩子**（不可能只有右孩子）。

---

## 📖 教材补充：树、森林与二叉树的转换（408选择题考点）

### 转换规则速记

| 转换方向 | 规则 |
|----------|------|
| 树 → 二叉树 | **左孩子右兄弟**：每个结点第一个孩子→左，下一个兄弟→右 |
| 森林 → 二叉树 | 各树根视为兄弟，右指针相连 |
| 二叉树 → 树 | 右指针变兄弟，左指针变孩子 |
| 二叉树 → 森林 | 沿根结点右链反复断开 |

### 408必背结论

- 树转换成的二叉树，其**根结点无右子树**（因为根没有兄弟）
- 二叉树无右子树，说明对应的原始结构是一棵树（而非森林）
- 树的**先根遍历** = 对应二叉树的**先序遍历**
- 树的**后根遍历** = 对应二叉树的**中序遍历**
- 森林的**先序遍历** = 对应二叉树的**先序遍历**
- 森林的**中序遍历** = 对应二叉树的**中序遍历**

---

## 📖 教材补充：二叉排序树的查找性能分析

| 树的形态 | 查找复杂度 | 发生条件 |
|----------|-----------|----------|
| 平衡（左右子树高度差≤1） | O(log n) | 随机数据、AVL树 |
| 退化成单链表 | O(n) | 插入有序序列 |
| 一般情况 | O(log n) 平均 | 大多数实际场景 |

> **408结论**：BST的查找效率取决于**树的高度**，而非结点数。

---

## 📖 教材补充：AVL旋转的平衡因子更新规律

| 旋转类型 | 旋转后BF变化 | 速记 |
|----------|-------------|------|
| LL（右单旋） | A.bf=B.bf=0（当BL高度为h时） | 单旋后BF归零 |
| RR（左单旋） | A.bf=B.bf=0 | 同上 |
| LR（先左后右） | 新根BF=0，A和B的BF取决于插入位置 | **双旋BF需分三种情况** |
| RL（先右后左） | 新根BF=0，A和B的BF取决于插入位置 | 同上 |

> **408注意**：AVL旋转后的平衡因子更新，**必须重新计算高度**而不是靠经验推断。手算时建议老老实实重算高度。

---

## 🔥 408真题中的树

| 年份 | 题型 | 考察内容 |
|------|------|----------|
| 2014 | 算法题 | 二叉树带权路径长度(WPL) |
| 2017 | 算法题 | 二叉树遍历的灵活运用 |
| 2019 | 选择题 | AVL树插入/旋转过程 |
| 2020 | 选择题 | 哈夫曼树WPL计算 |
| 2021 | 算法题 | BST的构建与查找 |
| 2022 | 选择题 | 完全二叉树性质 |
| 2023 | 算法题 | 二叉树的递归操作 |

---

> 🔗 上一章：[[DS-Ch4-串]] | 下一章：[[DS-Ch6-图]] | [[DS-大题模板]] | [[DS-MOC-数据结构总览|MOC]]
