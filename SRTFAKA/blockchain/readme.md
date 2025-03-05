# Blockchain Setup
Prerequisites: You will need Docker (Enable WSL2 integration), WSL2

## Go into WSL2 use Ubuntu-24.04 (I used this)

1. Open powershell as administrator

2. Install Ubuntu-24.04 on Windows Subsystem for Linux (WSL)

For those without Ubuntu 24.04
```
wsl --install -d Ubuntu-24.04 
```
3. Launch Ubuntu on WSL
```
wsl -d Ubuntu-24.04
```

4. In the WSL terminal, navigate to the location of the local repository with the following path
```
cd /mnt/c/[path to repo]/SkillsReadyTalentFutureAdamKhooAcademy/SRTFAKA/blockchain
```

5. Run the Hyperledger setup shell script
```
./setup_hyperledger.sh 
```

6. Create a network bridge between the Docker containers 

Go to *Docker Desktop* and execute the command in the docker terminal 
```
docker network create -d bridge fabric
```

Still got the GRPC side to do (WIP)


You should see this output

--> Submit Transaction: InitLedger, function creates the initial set of assets on the ledger
*** Transaction committed successfully

--> Evaluate Transaction: GetAllAssets, function returns all the current assets on the ledger
*** Result:[
  {
    "CertificateId": "1",
    "CourseID": "5",
    "Owner": "Tomoko"
  },
  {
    "CertificateId": "2",
    "CourseID": "5",
    "Owner": "Brad"
  },
  {
    "CertificateId": "3",
    "CourseID": "10",
    "Owner": "Jin Soo"
  },
  {
    "CertificateId": "4",
    "CourseID": "10",
    "Owner": "Max"
  },
  {
    "CertificateId": "5",
    "CourseID": "15",
    "Owner": "Adriana"
  },
  {
    "CertificateId": "6",
    "CourseID": "15",
    "Owner": "Michel"
  }
]

--> Submit Transaction: CreateAsset, creates new asset with CertificateId, CourseID and Owner arguments
*** Transaction committed successfully

--> Evaluate Transaction: ReadAsset, function returns asset attributes
*** Result:{
  "CertificateId": "1",
  "CourseID": "5",
  "Owner": "Tomoko"
}

--> Evaluate Transaction: GetAllAssets, function returns all the current assets on the ledger
*** Result:[
  {
    "CertificateId": "1",
    "CourseID": "5",
    "Owner": "Tomoko"
  },
  {
    "CertificateId": "1740682057052",
    "CourseID": "11",
    "Owner": "James"
  },
  {
    "CertificateId": "2",
    "CourseID": "5",
    "Owner": "Brad"
  },
  {
    "CertificateId": "3",
    "CourseID": "10",
    "Owner": "Jin Soo"
  },
  {
    "CertificateId": "4",
    "CourseID": "10",
    "Owner": "Max"
  },
  {
    "CertificateId": "5",
    "CourseID": "15",
    "Owner": "Adriana"
  },
  {
    "CertificateId": "6",
    "CourseID": "15",
    "Owner": "Michel"
  }
]