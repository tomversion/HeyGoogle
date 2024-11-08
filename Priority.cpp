#include<iostream>
using namespace std;

int main(){

    int np;
    cout<<"Enter the Number of Processes : ";
    cin>>np;

    int pid[np],at[np],bt[np],ct[np],tat[np],wt[np],pr[np],c[np];
    double tottat=0, totwt=0;

    for(int i=0;i<np;i++){

        cout<<"For Process "<<i+1<<":"<<endl;
        cout<<"Enter Process ID : ";
        cin>>pid[i];
        cout<<"Enter Process Arrival-Time : ";
        cin>>at[i];
        cout<<"Enter Process Burst-Time : ";
        cin>>bt[i];
        cout<<"Enter Process Priority : ";
        cin>>pr[i];
        c[i]=0;
    }

    int comp = 0,curt = 0;

    while(comp < np){

        int min_p=9999,p=-1;

        for(int i=0;i<np;i++){

            if(at[i]<=curt && !c[i] && pr[i]<min_p){
                min_p = pr[i];
                p = i;
            }

        }

        if(p == -1){
            curt++;
            continue;
        }

        c[p] = 1;
        comp++;

        curt += bt[p];
        ct[p] = curt;
        tat[p] = ct[p] - at[p];
        wt[p] = tat[p] - bt[p];

        tottat += tat[p];
        totwt += wt[p];

    }

    // 
    cout<<endl;
    cout<<"--------------------------------------------------------------------------------------"<<endl;
    cout<<"| PID | Priority | Arrival-Time | Burst-Time | Completion-Time | Turnaround-Time | Waiting-Time |"<<endl;
    cout<<"--------------------------------------------------------------------------------------"<<endl;
    for(int i=0;i<np;i++){
        cout<<"|  "<<pid[i]<<"  |    "<<pr[i]<<"    |     "<<at[i]<<"     |     "<<bt[i]<<"     |       "<<ct[i]<<"       |       "<<tat[i]<<"       |     "<<wt[i]<<"     |"<<endl;
    }
    cout<<"--------------------------------------------------------------------------------------"<<endl;
    cout<<endl;
    cout<<"--------------------------------------------------------------------------------------"<<endl;
    cout<<"Avrage Turnaround-Time is : "<<tottat/np<<endl;
    cout<<"Avrage Waiting-Time is : "<<totwt/np<<endl;
    cout<<"--------------------------------------------------------------------------------------"<<endl;
    cout<<endl;
    for(int i=0;i<np;i++){
        cout<<"+----";
    }
    cout<<"+"<<endl;
    for(int i=0;i<np;i++){
        cout<<"| P"<<pid[i]<<" ";
    }
    cout<<"|";
    cout<<endl;
    for(int i=0;i<np;i++){
        cout<<"+----";
    }
    cout<<"+"<<endl;
    cout<<"0    ";
    for(int i=0;i<np;i++){
        cout<<ct[i]<<"    ";
    }
    // 

    return 0;
}