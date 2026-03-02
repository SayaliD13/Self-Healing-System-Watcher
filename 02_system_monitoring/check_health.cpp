/* Title: System Health Monitor
Approach: This tool checks current RAM usage using Windows headers.
Work: If RAM usage is high (>80%), it prints 'UNHEALTHY', otherwise 'HEALTHY'. 
*/

#include <iostream>
#include <windows.h> 

using namespace std;

int main() 
{
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(MEMORYSTATUSEX);
    
    // Fetching system memory status
    if (GlobalMemoryStatusEx(&memInfo)) 
    {
        // dwMemoryLoad gives the percentage of memory in use
        int ramUsage = memInfo.dwMemoryLoad; 
        
        // Logical check for system stability
        if (ramUsage > 80) 
        {
            cout << "STATUS: UNHEALTHY | RAM Usage: " << ramUsage << "%" << endl;
        } 
        else 
        {
            cout << "STATUS: HEALTHY | RAM Usage: " << ramUsage << "%" << endl;
        }
    } 
    else 
    {
        cout << "ERROR: Failed to access system memory metrics." << endl;
        return 1;
    }

    return 0;
}