#include <iostream>
using namespace std;

const int MAX_PROCESSES = 10;
const int MAX_RESOURCES = 10;

bool isSafe(int allocation[MAX_PROCESSES][MAX_RESOURCES], 
            int max[MAX_PROCESSES][MAX_RESOURCES], 
            int need[MAX_PROCESSES][MAX_RESOURCES], 
            int available[MAX_RESOURCES], 
            int numProcesses, 
            int numResources) {
    
    bool finish[MAX_PROCESSES] = { false };
    int work[MAX_RESOURCES];
    
    for (int i = 0; i < numResources; i++) {
        work[i] = available[i];
    }

    int safeSequence[MAX_PROCESSES];
    int count = 0;

    while (count < numProcesses) {
        bool found = false;

        for (int p = 0; p < numProcesses; p++) {
            if (!finish[p]) {
                // Check if needs can be satisfied
                bool canAllocate = true;
                for (int r = 0; r < numResources; r++) {
                    if (need[p][r] > work[r]) {
                        canAllocate = false;
                        break;
                    }
                }

                if (canAllocate) {
                    // Simulate allocation
                    for (int r = 0; r < numResources; r++) {
                        work[r] += allocation[p][r];
                    }
                    finish[p] = true;
                    safeSequence[count++] = p;
                    found = true;
                }
            }
        }
        // If no process was found in this iteration, we are not in a safe state
        if (!found) {
            cout << "System is not in a safe state." << endl;
            return false;
        }   }
    // If we finish the loop, the system is in a safe state
    cout << "System is in a safe state.\nSafe sequence is: ";
    for (int i = 0; i < count; i++) {
        cout << safeSequence[i] << " ";
    }
    cout << endl;
    return true;
}
int main() {
    int numProcesses, numResources;
    cout << "Enter number of processes (max " << MAX_PROCESSES << "): ";
    cin >> numProcesses;
    if (numProcesses > MAX_PROCESSES) {
        cout << "Number of processes exceeds maximum limit." << endl;
        return 1;
    }

    cout << "Enter number of resources (max " << MAX_RESOURCES << "): ";
    cin >> numResources;
    if (numResources > MAX_RESOURCES) {
        cout << "Number of resources exceeds maximum limit." << endl;
        return 1;
    }
    int allocation[MAX_PROCESSES][MAX_RESOURCES];
    int max[MAX_PROCESSES][MAX_RESOURCES];
    int need[MAX_PROCESSES][MAX_RESOURCES];
    int available[MAX_RESOURCES];

    // Input Allocation matrix
    cout << "Enter allocation matrix:\n";
    for (int i = 0; i < numProcesses; i++) {
        for (int j = 0; j < numResources; j++) {
            cin >> allocation[i][j];
        }
    }
    // Input Max matrix
    cout << "Enter max matrix:\n";
    for (int i = 0; i < numProcesses; i++) {
        for (int j = 0; j < numResources; j++) {
            cin >> max[i][j];
        }
    }
    // Calculate Need matrix
    for (int i = 0; i < numProcesses; i++) {
        for (int j = 0; j < numResources; j++) {
            need[i][j] = max[i][j] - allocation[i][j];
        }
    }
    // Input Available resources
    cout << "Enter available resources:\n";
    for (int i = 0; i < numResources; i++) {
        cin >> available[i];
    }
    isSafe(allocation, max, need, available, numProcesses, numResources);
    return 0;
}

/*OUTPUT
Enter number of processes (max 10): 3
Enter number of resources (max 10): 3
Enter allocation matrix:
0 1 2
0 2 3
1 0 2
Enter max matrix:
2 1 0
1 2 3
3 0 2
Enter available resources:
3 3 3
System is in a safe state.
Safe sequence is: 0 1 2
*/