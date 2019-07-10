// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });

'use strict';

// Import the Dialogflow module from the Actions on Google client library.
// Import the Dialogflow module and response creation dependencies from the 
// Actions on Google client library.
const {
    dialogflow,
    Permission,
    Suggestions,
    BasicCard,
  } = require('actions-on-google');

// Import the required packages for deployment.
const functions = require('firebase-functions');
const fetch = require('node-fetch');


// Instantiate the Dialogflow client.
const app = dialogflow({debug: true});

app.intent('Default Welcome Intent', (conv) => {
    conv.ask(`Welcome! What can I help you with?`);
});

app.intent('person at the door', (conv) => {

    // endpoint that contains the list of people currently at the door
    const URL = 'https://eea00a58-6056-40c8-bad7-e40aeb5538f4.mock.pstmn.io/person';

    // retrieve the data from the endpoint
    return fetch(URL, {
        method: 'GET'
    }).then((response) => response.json())
    .then(data => {
        var people = data.name.split(',');
        if (people.length > 1) {
            conv.ask(`${people.join(', ')} are currently at the door.` +
            ` Would you like me to open the door for them?`);
            conv.ask(new Suggestions(`Yes`,`No`));
        } else if (people.length === 1) {
            conv.ask(`${people[0]} is currently at the door.` +
            ` Would you like me to open the door for ${people[0]}?`);
            conv.ask(new Suggestions(`Yes`,`No`));
        } else {
            conv.ask(`There is currently no one at the door. Did you need help with anything else?`);
            conv.ask(new Suggestions(`Yes`,`No`));
        }
        return null;
    });
});

app.intent('person at the door - yes', (conv) => {
    const URL = 'https://d20cdee3-84f6-43c3-a741-19c7f591b73e.mock.pstmn.io/lock';

    return fetch(URL, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.lock) {
            // unlocking the door
            putData(URL, {"lock":false})
            .then(data => console.log(JSON.stringify(data)))
            .catch(error => console.error(error));

            const audioSound = 'https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg';

            conv.ask(`<audio src="${audioSound}"></audio> ` + `<speak> The Door is now unlocked.` +
            `Is there anything else you needed help with? </speak>`);
            conv.ask(new Suggestions(`Yes`,`No`));
        } else {
            conv.ask(`The door is already unlocked. Is there anything else you need help with?`);
            conv.ask(new Suggestions(`Yes`,`No`));
        }
        return null;
    });
});

app.intent('lock_the_door', (conv) => {
    const URL = 'https://d20cdee3-84f6-43c3-a741-19c7f591b73e.mock.pstmn.io/lock';

    return fetch(URL, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.lock) {
            conv.ask(`The door is already locked. Is there anything else you need help with?`);
            conv.ask(new Suggestions(`Yes`,`No`));
        } else {
            // locking the door
            putData(URL, {"lock":true})
            .then(data => console.log(JSON.stringify(data)))
            .catch(error => console.error(error));

            const audioSound = 'https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg';

            conv.ask(`<audio src="${audioSound}"></audio> ` + `<speak> The Door is now locked.` +
            `Is there anything else you needed help with? </speak>`);
            conv.ask(new Suggestions(`Yes`,`No`));
        }
        return null;
    });
});

app.intent('unlock_the_door', (conv) => {
    const URL = 'https://d20cdee3-84f6-43c3-a741-19c7f591b73e.mock.pstmn.io/lock';

    return fetch(URL, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.lock) {
            // unlocking the door
            putData(URL, {"lock":false})
            .then(data => console.log(JSON.stringify(data)))
            .catch(error => console.error(error));

            const audioSound = 'https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg';

            conv.ask(`<audio src="${audioSound}"></audio> ` + `<speak> The Door is now unlocked.` +
            `Is there anything else you needed help with? </speak>`);
            conv.ask(new Suggestions(`Yes`,`No`));
        } else {
            conv.ask(`The door is already unlocked. Is there anything else you need help with?`);
            conv.ask(new Suggestions(`Yes`,`No`));
        }
        return null;
    });
});

app.intent('state_of_door', (conv) => {
    const URL = 'https://d20cdee3-84f6-43c3-a741-19c7f591b73e.mock.pstmn.io/lock';

    return fetch(URL, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.lock) {
            conv.ask(`The door is currently locked. Is there anything else you need help with?`);
            conv.ask(new Suggestions(`Yes`,`No`));
        } else {
            conv.ask(`The door is currently unlocked. Is there anything else you need help with?`);
        conv.ask(new Suggestions(`Yes`,`No`));
        }
        return null;
    });
});

// potentially add intent to confirm if someone is at the door
// eg. is jason at the door? 
// => no. jason is not at the door
// => jason is at the

function putData(url = '', data = {}) {
    const options = {
        method: 'PUT',
        body: JSON.stringify(data),
    }

    return fetch(url, options)
    .then(response => response.json());
}

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(app);