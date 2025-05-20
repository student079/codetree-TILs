#include <bits/stdc++.h>
using namespace std;

const int INF = numeric_limits<int>::max();

const int dRow[4] = {0, 1, 0, -1};
const int dCol[4] = {1, 0, -1, 0};

const int MAX_GRID_SIZE = 50;
const int MAX_JUMP_POWER = 5;

int gridSize, queryCount;

char lakeGrid[MAX_GRID_SIZE + 1][MAX_GRID_SIZE + 1];

int getStateId(int row, int col, int jumpPower) {
    return MAX_JUMP_POWER * ((row - 1) * gridSize + (col - 1)) + (jumpPower - 1);
}

vector<pair<int, int>> stateGraph[MAX_GRID_SIZE * MAX_GRID_SIZE * MAX_JUMP_POWER];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> gridSize;

    for (int row = 1; row <= gridSize; row++) {
        string rowString;
        cin >> rowString;

        for (int col = 1; col <= gridSize; col++) {
            lakeGrid[row][col] = rowString[col - 1];
        }
    }

    for (int row = 1; row <= gridSize; row++) {
        for (int col = 1; col <= gridSize; col++) {
            if (lakeGrid[row][col] != '.') {
                continue;
            }

            for (int jumpPower = 1; jumpPower <= MAX_JUMP_POWER; jumpPower++) {
                int currentState = getStateId(row, col, jumpPower);

                if (jumpPower < MAX_JUMP_POWER) {
                    int increasedJumpPower = jumpPower + 1;
                    int nextState = getStateId(row, col, increasedJumpPower);
                    int timeCost = increasedJumpPower * increasedJumpPower;
                    stateGraph[currentState].push_back({nextState, timeCost});
                }

                for (int newJumpPower = 1; newJumpPower < jumpPower; newJumpPower++) {
                    int nextState = getStateId(row, col, newJumpPower);
                    stateGraph[currentState].push_back({nextState, 1});
                }

                for (int direction = 0; direction < 4; direction++) {
                    int landingRow = row;
                    int landingCol = col;
                    bool validJump = true;

                    for (int step = 0; step < jumpPower; step++) {
                        landingRow += dRow[direction];
                        landingCol += dCol[direction];

                        if (landingRow < 1 || landingRow > gridSize || landingCol < 1 || landingCol > gridSize || lakeGrid[landingRow][landingCol] == '#') {
                            validJump = false;
                            break;
                        }
                    }

                    validJump = validJump && (lakeGrid[landingRow][landingCol] == '.');

                    if (validJump) {
                        int nextState = getStateId(landingRow, landingCol, jumpPower);
                        stateGraph[currentState].push_back({nextState, 1});
                    }
                }
            }

        }
    }

    cin >> queryCount;

    for (int query = 0; query < queryCount; query++) {
        int startRow, startCol, endRow, endCol;
        
        cin >> startRow >> startCol >> endRow >> endCol;

        int totalStates = gridSize * gridSize * MAX_JUMP_POWER;
        vector<int> distance(totalStates, INF);

        priority_queue<pair<int, int>, vector<pair<int,int>>, greater<pair<int, int>>> dijkstraPQ;
        int startState = getStateId(startRow, startCol, 1);
        distance[startState] = 0;
        dijkstraPQ.push({0, startState});
        int answerTime = INF;

        while (!dijkstraPQ.empty()) {
            auto [currentTime, currentState] = dijkstraPQ.top();
            dijkstraPQ.pop();

            if (distance[currentState] < currentTime) {
                continue;
            }

            int tempState = currentState;
            int currentJumpPower = (tempState % MAX_JUMP_POWER) + 1;
            tempState /= MAX_JUMP_POWER;
            int currentCol = (tempState % gridSize) + 1;
            tempState /= gridSize;
            int currentRow = (tempState % gridSize) + 1;

            if (currentRow == endRow && currentCol == endCol) {
                answerTime = currentTime;
                break;
            }

            for (auto &edge : stateGraph[currentState] ) {
                int nextState = edge.first;
                int transitionCost = edge.second;

                if (currentTime + transitionCost < distance[nextState] ) {
                    distance[nextState] = currentTime + transitionCost;
                    dijkstraPQ.push({distance[nextState], nextState});
                }
            }
        }

        cout << (answerTime < INF ? answerTime : -1) << "\n";
    }

    return 0;
}