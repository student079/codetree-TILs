#include <bits/stdc++.h>
using namespace std;

const int MAX_HEIGHT = 1000000;
const int SEG_TREE_SIZE = 4000005;

int segTree[SEG_TREE_SIZE];
int segIndex[SEG_TREE_SIZE];
vector<int> dpBuckets[MAX_HEIGHT + 1];
vector<int> mountainHeights;
vector<int> mountainDP;

void updateSegmentTree(int node, int segLeft, int segRight, int height, int dpValue) {
    if (height < segLeft || height > segRight) {
        return;
    }
    
    if (segLeft == segRight) {
        segTree[node] = dpValue;
        segIndex[node] = height;
        return;
    }

    int mid = (segLeft + segRight) / 2;
    updateSegmentTree(node * 2, segLeft, mid, height, dpValue);
    updateSegmentTree(node * 2 + 1, mid + 1, segRight, height, dpValue);

    if (segTree[node * 2] <= segTree[node * 2 + 1]) {
        segTree[node] = segTree[node * 2 + 1];
        segIndex[node] = segIndex[node * 2 + 1];
    }
    else {
        segTree[node] = segTree[node * 2];
        segIndex[node] = segIndex[node * 2];
    }
}

int querySegmentTree(int node, int segLeft, int segRight, int queryLeft, int queryRight) {
    if (segRight < queryLeft || segLeft > queryRight) {
        return 0;
    }

    if (queryLeft <= segLeft && segRight <= queryRight) {
        return segTree[node];
    }

    int mid = (segLeft + segRight) / 2;
    int leftQuery = querySegmentTree(node * 2, segLeft, mid, queryLeft, queryRight);
    int rightQuery = querySegmentTree(node * 2 + 1, mid + 1, segRight, queryLeft, queryRight);
    return max(leftQuery, rightQuery);
}

void initializeBoard(int numMountains, const vector<int>& initialMountains) {
    for (int height = 1; height <= MAX_HEIGHT; height++) {
        dpBuckets[height].push_back(0);
    }

    for (int i = 0; i < numMountains; i++) {
        int currentHeight = initialMountains[i];
        int dpValue = 1 + querySegmentTree(1, 1, MAX_HEIGHT,1, currentHeight - 1);

        dpBuckets[currentHeight].push_back(dpValue);
        mountainHeights.push_back(currentHeight);
        mountainDP.push_back(dpValue);
        updateSegmentTree(1, 1, MAX_HEIGHT, currentHeight, dpValue);
    }
}

void addMountain(int height) {
    int dpValue = 1 + querySegmentTree(1, 1, MAX_HEIGHT, 1, height - 1);

    dpBuckets[height].push_back(dpValue);
    mountainHeights.push_back(height);
    mountainDP.push_back(dpValue);
    updateSegmentTree(1, 1, MAX_HEIGHT, height, dpValue);
}

void removeLastMountain() {
    int height = mountainHeights.back();
    mountainHeights.pop_back();
    mountainDP.pop_back();
    dpBuckets[height].pop_back();

    int newDpValue = dpBuckets[height].back();
    updateSegmentTree(1, 1, MAX_HEIGHT, height, newDpValue);
}

void simulateHiking(int cableCarMountainIndex) {
    long long score = (long long) 1000000 * ( (mountainDP[cableCarMountainIndex - 1] - 1) + segTree[1]) + segIndex[1];
    cout << score << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int numQueries;
    cin >> numQueries;

    while(numQueries--) {
        int queryType;
        cin >> queryType;

        if (queryType == 100) {
            int numMountains;
            cin >> numMountains;
            vector<int> initialMountains;

            for (int i = 0; i < numMountains; i++) {
                int height;
                cin >> height;
                initialMountains.push_back(height);
            }
            initializeBoard(numMountains, initialMountains);
        }
        else if (queryType == 200) {
            int height;
            cin >> height;
            addMountain(height);
        }
        else if (queryType == 300) {
            removeLastMountain();
        }
        else if (queryType == 400) {
            int cableCarMountainIndex;
            
            cin >> cableCarMountainIndex;
            simulateHiking(cableCarMountainIndex);
        }
    }

    return 0;
}