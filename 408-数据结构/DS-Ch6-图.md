---
tags:
  - 408
  - 数据结构
  - Ch6
  - 图
  - BFS
  - DFS
  - 最短路径
  - 最小生成树
  - 拓扑排序
aliases:
  - DS第六章
  - 图
---

# DS-Ch6-图

> [[DS-MOC-数据结构总览|MOC]] | 上一章：[[DS-Ch5-树与二叉树]] | 下一章：[[DS-Ch7-查找]] | [[DS-大题模板]]

---

## 1. 图的基本概念

图 $G = (V, E)$，其中 $V$ 为顶点集，$E$ 为边集。

| 术语 | 含义 |
|------|------|
| 有向图 | 边有方向，$<v,w>$ 表示 $v \to w$ |
| 无向图 | 边无方向，$(v,w)$ 等价于 $(w,v)$ |
| 完全图 | 每对顶点间都有边。无向完全图 $n(n-1)/2$ 条边，有向完全图 $n(n-1)$ 条 |
| 连通图 | 无向图中任意两顶点间有路径 |
| 强连通图 | 有向图中任意两顶点间有双向路径 |
| 度 | 无向图：与顶点关联的边数；有向图：入度 + 出度 |
| 生成树 | 包含全部 $n$ 个顶点的极小连通子图，有 $n-1$ 条边 |

**度与边数的关系**（==408考点==）：
$$\sum \text{度} = 2|E| \quad \text{(无向图)} \qquad \sum \text{入度} = \sum \text{出度} = |E| \quad \text{(有向图)}$$

---

## 2. 图的存储

### 2.1 邻接矩阵

```c
//==408考点== 邻接矩阵存储结构定义
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAXV 100          // 最大顶点数
#define INF  INT_MAX      // 表示无穷大（无边）

// 邻接矩阵存储结构
typedef struct {
    int vexnum, arcnum;          // 顶点数，边数
    char vexs[MAXV];             // 顶点信息（可选）
    int edges[MAXV][MAXV];       // 邻接矩阵，edges[i][j] = 权值，无边为 INF
} MGraph;

//==408考点== 创建邻接矩阵（无向图示例）
void CreateMGraph(MGraph *G) {
    int i, j, w;
    printf("输入顶点数和边数: ");
    scanf("%d %d", &G->vexnum, &G->arcnum);

    // 初始化邻接矩阵：对角线为 0，其余为 INF
    for (i = 0; i < G->vexnum; i++) {
        for (j = 0; j < G->vexnum; j++) {
            if (i == j) G->edges[i][j] = 0;
            else        G->edges[i][j] = INF;
        }
    }

    //==408考点== 若为无向图，对称赋值
    printf("输入每条边 (起点 终点 权值)，顶点从 0 开始编号:\n");
    for (int k = 0; k < G->arcnum; k++) {
        scanf("%d %d %d", &i, &j, &w);
        G->edges[i][j] = w;
        G->edges[j][i] = w;        // 无向图对称；有向图去掉此行
    }
}
```

**邻接矩阵特点（==408考点==）**：
- 空间复杂度 $O(n^2)$，适合**稠密图**。
- 判断两顶点是否有边 $O(1)$。
- 求顶点的度：无向图扫描一行 $O(n)$；有向图出度扫描一行 + 入度扫描一列 $O(n)$。

---

### 2.2 邻接表

```c
//==408考点== 邻接表存储结构定义
#define MAXV 100

// 边表节点
typedef struct ArcNode {
    int adjvex;                  // 邻接点编号
    int weight;                  // 边的权值（网图使用）
    struct ArcNode *next;        // 下一条边
} ArcNode;

// 顶点表节点
typedef struct VNode {
    char data;                   // 顶点信息（可选）
    ArcNode *first;              // 第一条边
} VNode;

// 邻接表
typedef struct {
    VNode vertices[MAXV];        // 顶点表数组
    int vexnum, arcnum;          // 顶点数，边数
} ALGraph;

//==408考点== 创建邻接表（无向图，头插法）
void CreateALGraph(ALGraph *G) {
    printf("输入顶点数和边数: ");
    scanf("%d %d", &G->vexnum, &G->arcnum);

    // 初始化顶点表
    for (int i = 0; i < G->vexnum; i++) {
        G->vertices[i].first = NULL;
    }

    printf("输入每条边 (起点 终点)，顶点从 0 开始编号:\n");
    for (int k = 0; k < G->arcnum; k++) {
        int i, j;
        scanf("%d %d", &i, &j);

        //==408考点== 头插法：将新节点插入边表头部，O(1)
        // 插入边 (i -> j)
        ArcNode *p = (ArcNode *)malloc(sizeof(ArcNode));
        p->adjvex = j;
        p->weight = 1;
        p->next = G->vertices[i].first;
        G->vertices[i].first = p;

        // 无向图，插入反向边 (j -> i)
        ArcNode *q = (ArcNode *)malloc(sizeof(ArcNode));
        q->adjvex = i;
        q->weight = 1;
        q->next = G->vertices[j].first;
        G->vertices[j].first = q;
    }
}
```

**邻接表特点（==408考点==）**：
- 空间复杂度 $O(n+e)$，适合**稀疏图**。
- 判断两顶点是否有边需要遍历边表 $O(e/n)$（最坏 $O(n)$）。
- 求度：无向图 = 边表长度；有向图出度 = 边表长度，入度需**遍历所有边表**。
- 若要快速求入度，可用**逆邻接表**（==408考点==）。

---

## 3. DFS 深度优先遍历

### 3.1 DFS 递归实现（邻接矩阵 + 邻接表）

```c
// ==================== 邻接矩阵版 DFS ====================
//==408考点== DFS核心：递归 + visited数组防重复

int visited[MAXV];  // 全局访问标记数组

// 从顶点 v 出发，DFS 遍历邻接矩阵图
void DFS_MGraph(MGraph G, int v) {
    printf("%d ", v);          // 访问顶点
    visited[v] = 1;            //==408考点== 标记已访问，防止重复/死循环

    // 依次检查 v 的所有邻接点
    for (int j = 0; j < G.vexnum; j++) {
        if (G.edges[v][j] != INF && G.edges[v][j] != 0 && !visited[j]) {
            DFS_MGraph(G, j);  // 递归访问
        }
    }
}

// ==================== 邻接表版 DFS ====================
//==408考点== 邻接表的DFS，通过边表遍历邻接点

void DFS_ALGraph(ALGraph G, int v) {
    printf("%d ", v);
    visited[v] = 1;

    ArcNode *p = G.vertices[v].first;  // 取第一条边
    while (p != NULL) {
        if (!visited[p->adjvex]) {
            DFS_ALGraph(G, p->adjvex);
        }
        p = p->next;                   //==408考点== 沿边表链继续遍历
    }
}
```

### 3.2 非连通图的遍历（==408考点==）

```c
//==408考点== 非连通图：主调函数需对每个未访问顶点调用一次DFS
// 这样每个连通分量都会被遍历到

void DFSTraverse_MGraph(MGraph G) {
    // 初始化 visited 数组
    for (int i = 0; i < G.vexnum; i++) visited[i] = 0;

    for (int i = 0; i < G.vexnum; i++) {
        if (!visited[i]) {
            DFS_MGraph(G, i);   // 每调用一次，遍历一个连通分量
        }
    }
}

void DFSTraverse_ALGraph(ALGraph G) {
    for (int i = 0; i < G.vexnum; i++) visited[i] = 0;

    for (int i = 0; i < G.vexnum; i++) {
        if (!visited[i]) {
            DFS_ALGraph(G, i);
        }
    }
}
```

**考点总结**：
- 调用 DFS 函数的次数 = 连通分量个数。（==408考点==）
- DFS 生成树：遍历过程中经过的边构成树，回退的边为回边。
- 时间复杂度：邻接矩阵 $O(n^2)$，邻接表 $O(n+e)$。

---

## 4. BFS 广度优先遍历（队列实现）

```c
//==408考点== BFS：队列 + visited，类似树的层次遍历

// 简易循环队列
typedef struct {
    int data[MAXV];
    int front, rear;
} Queue;

void InitQueue(Queue *q) { q->front = q->rear = 0; }
int  QueueEmpty(Queue *q) { return q->front == q->rear; }
void EnQueue(Queue *q, int x) {
    q->data[q->rear] = x;
    q->rear = (q->rear + 1) % MAXV;       //==408考点== 循环队列取模
}
int DeQueue(Queue *q) {
    int x = q->data[q->front];
    q->front = (q->front + 1) % MAXV;
    return x;
}

// ==================== 邻接矩阵版 BFS ====================
void BFS_MGraph(MGraph G, int v) {
    Queue q;
    InitQueue(&q);

    printf("%d ", v);
    visited[v] = 1;
    EnQueue(&q, v);              //==408考点== 访问后立即入队

    while (!QueueEmpty(&q)) {
        int u = DeQueue(&q);     // 队首出队

        // 遍历 u 的所有邻接点
        for (int j = 0; j < G.vexnum; j++) {
            if (G.edges[u][j] != INF && G.edges[u][j] != 0 && !visited[j]) {
                printf("%d ", j);
                visited[j] = 1;
                EnQueue(&q, j);  //==408考点== 标记后立即入队
            }
        }
    }
}

// ==================== 邻接表版 BFS ====================
void BFS_ALGraph(ALGraph G, int v) {
    Queue q;
    InitQueue(&q);

    printf("%d ", v);
    visited[v] = 1;
    EnQueue(&q, v);

    while (!QueueEmpty(&q)) {
        int u = DeQueue(&q);
        ArcNode *p = G.vertices[u].first;

        while (p != NULL) {
            if (!visited[p->adjvex]) {
                printf("%d ", p->adjvex);
                visited[p->adjvex] = 1;
                EnQueue(&q, p->adjvex);
            }
            p = p->next;
        }
    }
}

//==408考点== BFS遍历非连通图
void BFSTraverse(ALGraph G) {
    for (int i = 0; i < G.vexnum; i++) visited[i] = 0;
    for (int i = 0; i < G.vexnum; i++) {
        if (!visited[i]) BFS_ALGraph(G, i);
    }
}
```

**考点**：
- BFS 求**无权图最短路径**（==408考点==）：BFS 按层访问，从起点到某顶点的层数 = 最短路径长度（边数）。
- BFS 生成树中不存在回边。

---

## 5. 最短路径

### 5.1 Dijkstra 算法（==408重点==）

**思想**：贪心。每次从未确定最短距离的顶点中选 **dist 最小**的加入已确定集合 $S$，并用它更新其邻接点的 dist。

**手算步骤模板**：
1. 初始化：$S = \{v_0\}$，$dist[v_0]=0$，其余 $\infty$。
2. 选 dist 最小且不在 $S$ 中的顶点 $u$，加入 $S$。
3. 对 $u$ 的每个邻接点 $w$ 不在 $S$ 中：若 $dist[u] + 边权 < dist[w]$，则**更新 dist[w] 并记录前驱**。
4. 重复 2-3 直到 $S$ 包含所有顶点。

```c
//==408考点== Dijkstra 完整实现（邻接矩阵）
// 求从顶点 v0 到其余各顶点的最短路径

void Dijkstra(MGraph G, int v0) {
    int dist[MAXV];             // dist[i] = v0 到 i 的最短距离
    int path[MAXV];             // path[i] = i 的前驱顶点，用于回溯路径
    int S[MAXV];                // S[i] = 1 表示顶点 i 已确定最短距离

    //==408考点== 初始化
    for (int i = 0; i < G.vexnum; i++) {
        dist[i] = G.edges[v0][i];        // 初始为直接距离
        S[i] = 0;
        if (G.edges[v0][i] != INF && i != v0)
            path[i] = v0;                // 有直连边则前驱为 v0
        else
            path[i] = -1;                // 无边则前驱为 -1
    }
    S[v0] = 1;                           // v0 自身已确定
    dist[v0] = 0;

    //==408考点== 主循环：每次确定一个顶点，共 n-1 次
    for (int k = 1; k < G.vexnum; k++) {
        // 步骤1: 选 dist 最小且未确定的顶点
        int minDist = INF;
        int u = -1;
        for (int i = 0; i < G.vexnum; i++) {
            if (!S[i] && dist[i] < minDist) {
                minDist = dist[i];
                u = i;
            }
        }
        if (u == -1) break;              // 剩余顶点不可达
        S[u] = 1;                        //==408考点== 将 u 加入已确定集合

        // 步骤2: 用 u 更新其邻接点的 dist
        for (int w = 0; w < G.vexnum; w++) {
            if (!S[w] && G.edges[u][w] != INF && G.edges[u][w] != 0) {
                //==408考点== 松弛操作：dist[u] + 边权 < dist[w] 则更新
                if (dist[u] + G.edges[u][w] < dist[w]) {
                    dist[w] = dist[u] + G.edges[u][w];
                    path[w] = u;         // 更新前驱
                }
            }
        }
    }

    // 输出结果
    printf("从顶点 %d 出发的最短路径:\n", v0);
    for (int i = 0; i < G.vexnum; i++) {
        printf("到 %d: dist=%d, 路径: ", i, dist[i]);
        // 回溯输出路径（==408考点== 可能考察路径还原）
        int stack[MAXV], top = -1;
        int cur = i;
        while (cur != -1) {
            stack[++top] = cur;
            cur = path[cur];
        }
        while (top >= 0) printf("%d ", stack[top--]);
        printf("\n");
    }
}
```

**Dijkstra 手算演示**（==408考点==）：

```
图:   0 --4-- 1 --1-- 2
      |       |       |
      2       3       |
      |       |       |
      3 --5-- 4       |

邻接矩阵:
    0  1  2  3  4
0   0  4  ∞  2  ∞
1   4  0  1  ∞  3
2  ∞  1  0  ∞  ∞    (假定 2-3 无边)
3   2  ∞  ∞  0  5
4  ∞  3  ∞  5  0

初始: S={0}, dist=[0,4,∞,2,∞]
第1轮: min=dist[3]=2, 加入3 → S={0,3}
        用3更新: dist[4] = min(∞, 2+5=7) = 7
第2轮: min=dist[1]=4, 加入1 → S={0,3,1}
        用1更新: dist[2]=min(∞, 4+1=5)=5
第3轮: min=dist[2]=5, 加入2 → S={0,3,1,2}
        用2更新: 无
第4轮: min=dist[4]=7, 加入4 → S={0,3,1,2,4}
结果: dist = [0, 4, 5, 2, 7]
```

**考点提示**：
- 边权**不能为负**（==408考点==）。
- 每次选出顶点后不可再更改（已确定）。
- 时间复杂度：$O(n^2)$（邻接矩阵），用堆优化 $O((n+e)\log n)$。

---

### 5.2 Floyd 算法（思想，==408考点==）

```c
//==408考点== Floyd: 动态规划，求所有顶点对间的最短路径
// 核心: 对每一对 (i,j)，尝试以 k 为中间点是否更短

void Floyd(MGraph G, int dist[MAXV][MAXV], int path[MAXV][MAXV]) {
    // 初始化
    for (int i = 0; i < G.vexnum; i++) {
        for (int j = 0; j < G.vexnum; j++) {
            dist[i][j] = G.edges[i][j];
            path[i][j] = (G.edges[i][j] < INF) ? i : -1;
        }
    }

    //==408考点== 三重循环: k 在最外层（递推中间点）
    for (int k = 0; k < G.vexnum; k++) {
        for (int i = 0; i < G.vexnum; i++) {
            for (int j = 0; j < G.vexnum; j++) {
                // 防止溢出: 先判断是否可达
                if (dist[i][k] != INF && dist[k][j] != INF
                    && dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                    path[i][j] = path[k][j];  //==408考点== 前驱更新
                }
            }
        }
    }
}
```

**Floyd 特点（==408考点==）**：
- 允许负权边，但**不允许负权回路**。
- 时间复杂度 $O(n^3)$，适合稠密图。
- 可检测负权回路：完成后检查 $dist[i][i] < 0$ 的顶点。

**Dijkstra vs Floyd 对比**：

| 算法 | 求解范围 | 时间复杂度 | 负权边 | 负权回路 |
|------|----------|-----------|--------|----------|
| Dijkstra | 单源 | $O(n^2)$ | 不允许 | 不允许 |
| Floyd | 所有顶点对 | $O(n^3)$ | 允许 | 不允许 |

---

## 6. 最小生成树（MST）

### 6.1 Prim 算法（思想 + 手算）

**思想**（==408考点==）：贪心。从任意顶点开始，每次选**连接已选集合与未选集合的最小权边**，将边和顶点加入。

**手算步骤**：
1. 任选一个起点，加入集合 $U$。
2. 在所有 $u \in U, v \notin U$ 的边 $(u,v)$ 中，选权值最小的，将 $v$ 加入 $U$。
3. 重复直到 $U$ 包含全部顶点。

**手算演示**：

```
     A -2- B
    /|     |\
   3 4     1 5
  /  |     |  \
 C-6-D-3-E-7-F

Prim 从 A 开始:
U={A}:  候选边 A-B(2), A-C(3), A-D(4) → 选 A-B(2)
U={A,B}: 候选边 A-C(3), A-D(4), B-E(1), B-F(5) → 选 B-E(1)
U={A,B,E}: 候选边 A-C(3), A-D(4), B-F(5), E-D(3), E-F(7) → 选 A-C(3) 或 E-D(3)
...最终得到 MST
```

**Prim 时间复杂度**：邻接矩阵 $O(n^2)$，适合**稠密图**。

---

### 6.2 Kruskal 算法（思想 + 手算）

**思想**（==408考点==）：贪心 + 并查集。**对所有边按权值排序**，依次选最小的，若边的两端不在同一连通分量中则加入 MST。

**手算步骤**：
1. 所有边按权值从小到大排序。
2. 依次检查每条边：若两端不在同一集合则选取，否则跳过。
3. 选够 $n-1$ 条边时停止。

**手算演示（同上图）**：

```
所有边排序（权值）:
B-E(1), A-B(2), A-C(3), D-E(3), C-D(6), B-F(5), A-D(4), E-F(7)

依次选取:
B-E(1): 连通分量 {B,E}  → 选
A-B(2): A 与 B 不在同集合 → 选，{A,B,E}
A-C(3): A 与 C 不在同集合 → 选，{A,B,C,E}
D-E(3): D 与 E 不在同集合 → 选，{A,B,C,D,E}
B-F(5): F 与 B 不在同集合 → 选，{全连通}
已选 5 条 = n-1 = 5，停止。
MST 权值和 = 1+2+3+3+5 = 14
```

**Kruskal 时间复杂度**：$O(e \log e)$（排序主导），适合**稀疏图**。

**Prim vs Kruskal**：

| 算法 | 策略 | 时间复杂度 | 适合 |
|------|------|-----------|------|
| Prim | 选顶点（离集合最近） | $O(n^2)$ | 稠密图 |
| Kruskal | 选边（权值最小） | $O(e \log e)$ | 稀疏图 |

---

## 7. 拓扑排序（==408考点==）

**AOV 网**：顶点表示活动，有向边表示活动间先后关系。

```c
//==408考点== 拓扑排序：入度表法，输出序列不唯一
// 步骤: 1) 计算所有顶点入度 2) 入度为0的入栈 3) 出栈并更新邻接点入度

int TopologicalSort(ALGraph G, int topo[]) {
    int indegree[MAXV] = {0};   // 入度数组
    int stack[MAXV], top = -1;  // 栈存放入度为 0 的顶点
    int count = 0;              // 已输出顶点数

    // 步骤1: 计算所有顶点入度（==408考点== 遍历所有边表）
    for (int i = 0; i < G.vexnum; i++) {
        ArcNode *p = G.vertices[i].first;
        while (p != NULL) {
            indegree[p->adjvex]++;   // 每出现一条 i->adjvex 的边，入度+1
            p = p->next;
        }
    }

    // 步骤2: 入度为 0 的顶点入栈
    for (int i = 0; i < G.vexnum; i++) {
        if (indegree[i] == 0) stack[++top] = i;
    }

    // 步骤3: 出栈→输出→更新入度（==408考点== 核心循环）
    while (top != -1) {
        int u = stack[top--];        // 弹出
        topo[count++] = u;           // 输出

        // 将 u 的所有邻接点入度减 1
        ArcNode *p = G.vertices[u].first;
        while (p != NULL) {
            int w = p->adjvex;
            indegree[w]--;           //==408考点== 入度减1
            if (indegree[w] == 0) {  // 若变为0则入栈
                stack[++top] = w;
            }
            p = p->next;
        }
    }

    //==408考点== 若 count < vexnum，说明图中有回路
    if (count < G.vexnum) {
        printf("图中存在回路，无法完成拓扑排序!\n");
        return 0;                    // 失败
    }
    return 1;                        // 成功
}
```

**拓扑排序考点**：
- 使用栈则输出逆偏序，使用队列则输出偏序（==408考点==）。
- 若存在回路（环），必然有顶点无法入栈，最终输出数 < n。
- 用 DFS 也可实现拓扑排序：在 DFS 回溯时将顶点入栈，最后逆序输出。

---

## 8. 关键路径（AOE 网，手算）

**AOE 网**：边表示活动，顶点表示事件，边权为活动持续时间。

**四个关键量**（==408考点==）：

| 量 | 含义 | 计算方向 |
|----|------|----------|
| $ve(k)$ | 事件 $k$ **最早**发生时间 | 源点→汇点，**取 max** |
| $vl(k)$ | 事件 $k$ **最迟**发生时间 | 汇点→源点，**取 min** |
| $e(i)$ | 活动 $i$ **最早**开始时间 = $ve(\text{弧尾})$ | —— |
| $l(i)$ | 活动 $i$ **最迟**开始时间 = $vl(\text{弧头}) - \text{权}$ | —— |

**关键活动**：$e(i) = l(i)$ 的活动，即没有时间余量。

**手算步骤**（==408考点==）：

```
示例 AOE 网:
    v1 --a1=3--> v2 --a2=2--> v4
     \                         ^
      a4=2                     |
       \                       |
        v3 ------a3=4--------->+

1. 求 ve（从源点开始，向前递推）:
   ve(v1) = 0
   ve(v2) = ve(v1)+3 = 3
   ve(v3) = ve(v1)+2 = 2
   ve(v4) = max(ve(v2)+2, ve(v3)+4) = max(5, 6) = 6

2. 求 vl（从汇点开始，向后递推）:
   vl(v4) = ve(v4) = 6
   vl(v3) = vl(v4)-4 = 2
   vl(v2) = vl(v4)-2 = 4
   vl(v1) = min(vl(v2)-3, vl(v3)-2) = min(1, 0) = 0

3. 求 e 和 l:
   a1(v1→v2): e=ve(v1)=0, l=vl(v2)-3=4-3=1 → 非关键
   a2(v2→v4): e=ve(v2)=3, l=vl(v4)-2=6-2=4 → 非关键
   a4(v1→v3): e=ve(v1)=0, l=vl(v3)-2=2-2=0 → 关键！
   a3(v3→v4): e=ve(v3)=2, l=vl(v4)-4=6-4=2 → 关键！

4. 关键路径: v1 → v3 → v4，总时长为 6
```

**考点提示**：
- 关键路径可能有多条，缩短公共关键活动才有效。
- 缩短某关键活动时间可能使关键路径改变。
- 若关键活动耗时减少，需**重新计算**关键路径。
- $ve$ 取 max，$vl$ 取 min（==408易错==）。

---

## 9. 复杂度对比表（==408考点==）

| 操作/算法 | 邻接矩阵 | 邻接表 |
|-----------|---------|--------|
| 存储空间 | $O(n^2)$ | $O(n+e)$ |
| 判断 $(u,v)$ 是否有边 | $O(1)$ | $O(e/n) \sim O(n)$ |
| 遍历某顶点的所有邻接点 | $O(n)$ | $O(\text{出度})$ |
| DFS 时间复杂度 | $O(n^2)$ | $O(n+e)$ |
| BFS 时间复杂度 | $O(n^2)$ | $O(n+e)$ |
| Prim 时间复杂度 | $O(n^2)$ | $O(n^2)$ (需特殊优化) |
| Dijkstra 时间复杂度 | $O(n^2)$ | $O(n^2)$ / 堆优化 $O((n+e)\log n)$ |
| 适合场景 | 稠密图 | 稀疏图 |

---

## 10. 408 易错点

1. **连通分量 vs 连通图**：无向图的极大连通子图叫连通分量；有向图的极大强连通子图叫强连通分量。连通图的连通分量是其自身（仅1个）。（==408考点==）

2. **生成树边数**：$n$ 个顶点的生成树有 $n-1$ 条边，多一条则成环，少一条则不连通。（==408考点==）

3. **DFS/BFS 遍历非连通图**：调用 DFS/BFS 的次数 = 连通分量数。务必在主函数中对所有未访问顶点进行遍历。（==408考点==）

4. **Dijkstra 负权边**：Dijkstra 不允许负权边，因为已确定最短距离的顶点可能被负权边再次缩短。含负权边用 Bellman-Ford。（==408考点==）

5. **Floyd 三层循环顺序**：$k$ 必须在最外层，表示"允许经过前 $k$ 个顶点中转"。顺序错误会导致结果错误。（==408考点==）

6. **拓扑排序 vs 逆拓扑排序**：拓扑排序是入度为 0 的顶点先输出；DFS 回溯顺序的逆序也是一个拓扑序列。（==408考点==）

7. **关键路径的 ve/vl 方向**：$ve$ 从源点开始向前递推（取 max），$vl$ 从汇点开始向后递推（取 min）。方向记反则全错。（==408考点==）

8. **邻接表求入度**：有向图邻接表求入度需遍历所有边表，$O(n+e)$。考试中若需频繁求入度，应使用逆邻接表或十字链表。（==408考点==）

9. **最小生成树唯一性**：当图中所有边权值互不相等时，MST 唯一。有权值相等的边时 MST 可能不唯一。（==408考点==）

10. **BFS 求最短路径的前提**：仅当图为**无权图**（或所有边权相等）时，BFS 按层扩展才等价于最短路径。有权图必须用 Dijkstra。（==408考点==）

---

## 11. 完整测试主函数

```c
//==408考点== 综合测试：按需注释/取消注释各部分

int main() {
    ALGraph G_AL;
    MGraph G_M;

    printf("===== 邻接表创建与遍历 =====\n");
    CreateALGraph(&G_AL);

    printf("DFS (邻接表): ");
    for (int i = 0; i < G_AL.vexnum; i++) visited[i] = 0;
    for (int i = 0; i < G_AL.vexnum; i++)
        if (!visited[i]) DFS_ALGraph(G_AL, i);
    printf("\n");

    printf("BFS (邻接表): ");
    BFSTraverse(G_AL);
    printf("\n");

    printf("===== 拓扑排序 =====\n");
    int topo[MAXV];
    if (TopologicalSort(G_AL, topo)) {
        printf("拓扑序列: ");
        for (int i = 0; i < G_AL.vexnum; i++)
            printf("%d ", topo[i]);
        printf("\n");
    }

    printf("===== 邻接矩阵 + Dijkstra =====\n");
    CreateMGraph(&G_M);
    Dijkstra(G_M, 0);

    return 0;
}
```

---

## 🎯 力扣推荐

| 题目 | 难度 | 推荐理由 | 408考点关联 |
|------|------|----------|------------|
| [200. 岛屿数量](https://leetcode.cn/problems/number-of-islands/) | 中等 | ⭐ **DFS/BFS四方向遍历** | 408中图的DFS/BFS遍历应用 |
| [994. 腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/) | 中等 | 多源BFS | 408中BFS的层级扩展 |
| [207. 课程表](https://leetcode.cn/problems/course-schedule/) | 中等 | ⭐ **拓扑排序** | 408拓扑排序（有环判断） |
| [210. 课程表 II](https://leetcode.cn/problems/course-schedule-ii/) | 中等 | 拓扑排序输出序列 | 408拓扑排序应用 |
| [133. 克隆图](https://leetcode.cn/problems/clone-graph/) | 中等 | DFS/BFS+哈希表 | 408图的遍历综合题 |
| [547. 省份数量](https://leetcode.cn/problems/number-of-provinces/) | 中等 | **连通分量计数** | 408调用DFS次数=连通分量数 |
| [797. 所有可能的路径](https://leetcode.cn/problems/all-paths-from-source-to-target/) | 中等 | DFS路径搜索 | 408中路径搜索 |
| [743. 网络延迟时间](https://leetcode.cn/problems/network-delay-time/) | 中等 | **Dijkstra求最短路径** | 408 Dijkstra直接应用 |

### 刷题建议

> 💡 你有编程基础，图这部分力扣题的实现风格与408差异较大（力扣多用邻接表构建、面向对象），建议重点关注**算法思想本身**而非代码细节。
>
> 必做：200（DFS/BFS）、207（拓扑排序）、547（连通分量）、743（Dijkstra）
> 选做：其他用于巩固理解

---

## 🔥 408与力扣的差异

| 方面 | 力扣 | 408 |
|------|------|-----|
| 图的存储 | 通常用邻接表(动态列表) | 邻接矩阵和静态链式邻接表都考 |
| 遍历实现 | 递归DFS/迭代BFS皆可 | 必须掌握两种存储结构下的实现 |
| 算法手算 | 不要求 | **Dijkstra和关键路径要求手算** |
| 顶点编号 | 0-based | 两种都可能，看清题目 |
| 完整代码 | 只要求核心逻辑 | 要求**结构体定义+函数实现+复杂度标注** |

---

## 📖 教材补充：图的遍历与连通性

### 无向图的连通性与DFS/BFS调用次数

- 调用DFS/BFS的次数 = **连通分量数**
- 每调用一次遍历一个连通分量

### 有向图的强连通性

- **强连通图**：任意两点间都有双向路径
- **强连通分量**：极大强连通子图
- Kosaraju算法：对原图DFS→按完成时间逆序→对转置图DFS（两次DFS找强连通分量）
- **408考点**：不要求写出Kosaraju完整代码，但要知道"两次DFS可以找强连通分量"

### 生成树与生成森林

- **生成树**：包含所有n个顶点的极小连通子图，n-1条边
- **生成森林**：非连通图每个连通分量的生成树组成
- **最小生成树**：权值和最小的生成树，不唯一（当有权值相等的边时）

---

## 📖 教材补充：最短路径算法细节

### Dijkstra不适用于负权边的本质原因

Dijkstra的贪心策略：每次选dist最小的顶点加入S，并断言其dist已确定。
- 如果有负权边，可能出现：一个已确定dist的顶点，通过负权边+其他顶点变得**更短**。
- **408考点**：含负权边时用Bellman-Ford算法（408了解思想即可，不要求代码）

### Floyd算法的路径还原

```c
// 通过path矩阵还原 i→j 的完整路径
void PrintPath(int path[MAXV][MAXV], int i, int j) {
    if (path[i][j] == -1) return;
    int mid = path[i][j];
    PrintPath(path, i, mid);
    printf("%d ", mid);
    PrintPath(path, mid, j);
}
// 调用：printf("%d ", i); PrintPath(path, i, j); printf("%d ", j);
```

---

## 📖 教材补充：最小生成树的正确性证明思想

| 算法 | 策略 | 证明思想（了解即可） |
|------|------|---------------------|
| Prim | 选顶点（离集合最近） | 切割性质：连接U和V-U的最小权边一定在MST中 |
| Kruskal | 选边（权值最小） | 回路性质：环中最大权边一定不在MST中 |

---

## 📖 教材补充：关键路径的进一步说明

| 概念 | 说明 |
|------|------|
| 关键路径 | AOE网中从源点到汇点的最长路径（决定了最短工期） |
| 关键活动 | e(i)=l(i)的活动，即时间余量为0 |
| 关键路径特点 | 可能有多条；**缩短公共关键活动才有效** |
| 注意事项 | 缩短关键活动后需**重新计算关键路径** |

---

## 🔥 408真题中的图

| 年份 | 题型 | 考察内容 |
|------|------|----------|
| 2012 | 选择题 | Dijkstra手算过程 |
| 2014 | 算法题 | 图的邻接表存储+DFS |
| 2015 | 选择题 | 拓扑排序 |
| 2018 | 选择题 | 最小生成树(Kruskal) |
| 2019 | 选择题 | 关键路径ve/vl计算 |
| 2020 | 选择题 | Floyd算法 |
| 2021 | 算法题 | 图的遍历与判断 |
| 2023 | 选择题 | Dijkstra与Floyd对比 |

---

## 📖 教材补充：最短路径长度计算技巧

在无权图中（或所有边权相等），BFS按层扩展，从起点到某顶点的**层数 = 最短路径长度**。这一结论在408的选择题中经常用到。

另外注意Dijkstra算法在执行过程中，**每一轮确定的顶点就是当前dist最小的顶点**，这个顶点一旦加入S集合就不会再改变。

---

> 🔗 上一章：[[DS-Ch5-树与二叉树]] | 下一章：[[DS-Ch7-查找]] | [[DS-大题模板]] | [[DS-MOC-数据结构总览|MOC]]
