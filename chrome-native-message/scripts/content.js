


let queue = [];
let doneTimer = null;
const processedPairs = new Set();

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    console.log("change");
    if (mutation.type === 'childList' && mutation.addedNodes.length > 0){
      mutation.addedNodes.forEach((node) => {
    //   // Only process actual elements (ignore text/comments)
        if (node.nodeType === Node.ELEMENT_NODE) {
        
        // 1. Check if the added node itself is the span
        // if (node.matches('span.Grouping-styles__title')) {
        //   // className = node.textContent.trim()
        //   // console.log(className);
        //   processElement(node);
        // }

        const group = node.querySelectorAll('div.Grouping-styles__root.Grouping-styles__medium.planner-grouping');
        group.forEach((nested) => {
          const subject = nested.querySelector('span.Grouping-styles__title');

          const assignment = nested.querySelector('a.css-18p5viu-view-link span:nth-of-type(1)');
          const assignmentNameNode = nested.querySelector('a.css-18p5viu-view-link span:nth-of-type(2)');


          if (subject && assignment && assignmentNameNode) {
            const subjectName = subject.textContent.trim();
            const assignmentName = assignmentNameNode.textContent.trim();
            const pairKey = `${subjectName} -> ${assignmentName}`;

            if (!processedPairs.has(pairKey)) {
              processedPairs.add(pairKey);
              assignmentDetatils = separateDetails(assignment, assignmentName);
              processAssaignment(subjectName, assignmentDetatils);
              timer();
            }
          }
        });

        // const classes = node.querySelectorAll('span.Grouping-styles__title');
        // classes.forEach(nested => processElement(nested));

        //NOTE: maybe put in own array bc it's your own tasks
        // const own_tasks = node.querySelectorAll('button.css-c4zpq1-view-link');
        // own_tasks.forEach(nested => processAssaignment(nested));


        // const assignments = node.querySelectorAll('a.css-18p5viu-view-link span:nth-of-type(2)');
        // assignments.forEach(nested => processElement(nested));

        };
      });
    };
  });
});

function separateDetails(detailsNode, name) {
  infoList = [];

  details = detailsNode.textContent.trim();
  
  infoList.push(name);

  taskNameLength = name.length;
  nameInd = details.indexOf(name);

  otherDetails = details.substring(nameInd+taskNameLength);

  if (otherDetails.includes("due")) {
    taskType = "assignment";
    typeLength = ", due ".length;
  }
  else if (otherDetails.includes("posted")) {
    taskType = "announcement";
    typeLength = " posted ".length;
  }

  timeDateDetails = otherDetails.substring(typeLength);
  
  spaceCount = 3;
  count = 0;
  timeDetails = timeDateDetails;
  while (count <= spaceCount) {
    spaceInd = timeDetails.indexOf(" ");
    timeDetails = timeDetails.substring(spaceInd+1);
    count++;
  }

  timeDetails = timeDetails.substring(0, timeDetails.length-1);
  timeInd = timeDateDetails.indexOf(timeDetails);
  dateDetails = timeDateDetails.substring(0,timeInd).trim();
  
  infoList.push(dateDetails);
  infoList.push(timeDetails);

  return infoList;
}

// Helper function to handle the found elements
function processAssaignment(classes, info) {
  taskName = info[0];
  taskDate = info[1];
  taskTime = info[2];

  fullTask = classes + ": " + taskName;

  taskDict = {'task': fullTask, 'date': taskDate, 'time': taskTime};
  queue.push(taskDict);
}

// function processElement(el){
//   if (el.matches('span.Grouping-styles__title')){
//     className = el.textContent.trim()
//     console.log(className);
//     console.log(assignmentName);
//   }
//   else if (el.matches('a.css-18p5viu-view-link span:nth-of-type(2)')){
//     assignmentName = el.textContent.trim()
//     // console.log(assignmentName);
//   }

//   if (className && assignmentName){
//     full_task = className + ": " + assignmentName;
//     send_msg_to_bgscript(full_task);
//   }
  // console.log(el);
  // send_msg_to_bgscript(el.textContent.trim());
// }
 
function timer(){
  doneTimer = setTimeout(() => {
        // console.log("No new changes for seconds.");
        if (queue.length > 0) {
          send_msg_to_bgscript(queue);
        }
    }, 500);
}

function send_msg_to_bgscript(info)
  {
    console.log(info);
    chrome.runtime.sendMessage({ action: "sendAssignment", data: info});
    queue = [];
  }
// Start observing
observer.observe(document.body, { 
  childList: true, 
  subtree: true,
  characterData: true 
});


