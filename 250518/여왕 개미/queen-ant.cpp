#include <bits/stdc++.h>
using namespace std;

// 이분탐색
// 좌표 0 ~ 1,000,000,000 10억
// 개미집 1 ~ N 10,000 1만
// Q 20,000 2만

int Q;
vector<bool> antHouseDelited(1);
vector<int> antHousePositions(1);

void initialVillageConstruction() {
    int numInitialAntHouses;
    cin >> numInitialAntHouses;

    for (int i = 1; i <= numInitialAntHouses; i++) {
        int position;
        cin >> position;

        antHousePositions.push_back(position);
        antHouseDelited.push_back(false);
    }
}

void addNewAntHouse() {
    int newAntHousePosition;
    cin >> newAntHousePosition;

    antHousePositions.push_back(newAntHousePosition);
    antHouseDelited.push_back(false);
}

void removeAntHouse() {
    int antHouseNumber;
    cin >> antHouseNumber;

    antHouseDelited[antHouseNumber] = true;
}

void processScout() {
    int numAnts;
    cin >> numAnts;

    int left = 0;
    int right = 1000000000;
    int minimumTime = 0;

    while (left <= right) {
        int midTime= (left + right) / 2;
        int intervalNeeded = 0;
        int lastCoveredPosition = -1000000000;

        for (size_t i = 1; i < antHousePositions.size(); i++) {
            if (antHouseDelited[i]) {
                continue;
            }

            int currentAntHousePosition = antHousePositions[i];

            if ( currentAntHousePosition - lastCoveredPosition > midTime) {
                intervalNeeded++;
                lastCoveredPosition = currentAntHousePosition;
            }
        }

        if (intervalNeeded <= numAnts) {
            minimumTime = midTime;
            right = midTime - 1;
        } else {
            left = midTime + 1;
        }
    }
    
    cout << minimumTime << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> Q;

    while(Q--) {
        int commandType;
        cin >> commandType;

        if (commandType == 100) {
            // 마을 건설
            initialVillageConstruction();
        }
        else if (commandType == 200) {
            // 개미집 건설
            addNewAntHouse();
        }
        else if (commandType == 300) {
            // 개미집 철거
            removeAntHouse();
        }
        else if (commandType == 400) {
            // 개미집 정찰
            processScout();
        } 
    }

    return 0;
}