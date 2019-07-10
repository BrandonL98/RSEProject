# RSEProject - Smart Door Unlock

# To get started
### Setting up firebase
Follow the tutorial on how to set up a firebase account on your laptop.
https://codelabs.developers.google.com/codelabs/actions-2/index.html?index=..%2F..index#1


### Setting up the working directory

If the current directory is not set up with firebase yet, the following steps will help initialise the directory for you. In the directory you want to work in, type
```
firebase init
select functions
select the firebase project (actions-lockagent-ea0fb (actions-lockagent))
javascript
yes
yes
```
Following the above commands should initialise the directory with a firebase.json and functions directory. Go into the functions directory.
```
cd functions
```
Functions folder contains an index.js file file, package.json file and a node-modules folder. The node-modules folder contains all the npm dependicies required for the program. Index.js is the primary file we will be working on. 

# Running the program
We first need to declare which agent we are working with.
```
firebase use --project actions-lockagent-ea0fb
```
After this, run the following steps to compile and deploy our files into the google cloud.
```
npm install
firebase deploy --project actions-lockagent-ea0fb
```
The file is now updated on the firebase server. On dialogflow, the intents should reply with the updated conversation responses declared in the index.js file. 


