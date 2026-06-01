



// const processedText = new Set();

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === 'childList' && mutation.addedNodes.length > 0){
      mutation.addedNodes.forEach((node) => {
    //   // Only process actual elements (ignore text/comments)
        if (node.nodeType === Node.ELEMENT_NODE) {
          // className = "";
          // assignmentName = "";
        
        // 1. Check if the added node itself is the span
        if (node.matches('span.Grouping-styles__title')) {
          // className = node.textContent.trim()
          // console.log(className);
          processElement(node);
        }

          // const classes = document.querySelector('span.Grouping-styles__title');
          // const assignment = document.querySelector('a.css-18p5viu-view-link span:nth-of-type(2)');         
          
          // if (classes && assignment){

          //   className = classes.textContent.trim();
          //   assignmentName = assignment.textContent.trim();

          //   processAssaignment(className,assignmentName);
          // }

        // 2. IMPORTANT: Search for any target spans HIDDEN inside this new node
        const classes = node.querySelectorAll('span.Grouping-styles__title');
        classes.forEach(nested => processElement(nested));

        //NOTE: maybe put in own array bc it's your own tasks
        // const own_tasks = node.querySelectorAll('button.css-c4zpq1-view-link');
        // own_tasks.forEach(nested => processAssaignment(nested));
        // if (node.matches('a.css-18p5viu-view-link')) {
        //   assignmentName = node.textContent.trim()
        //   // processElement(node);
        // }
        // const assignments = node.querySelector('a.css-18p5viu-view-link');
        // console.log(assignments);
        // assignmentName = assignments.textContent.trim();

        // assignments.forEach(nested => processAssaignment(nested));
        };
      });
    };
  });

});
// Helper function to handle the found elements
schoolClasses = []
function processAssaignment(classes, task) {
    full_task = classes + ": " + task;
    send_msg_to_bgscript(full_task);
}

function processElement(el){
  // schoolClasses.push(el.textContent.trim());
  // console.log(el.textContent.trim());
  send_msg_to_bgscript(el.textContent.trim());
}
// function 
// function timer(){
//   doneTimer = setTimeout(() => {
//         console.log("No new changes for 5 seconds.");
//         // observer.disconnect();
//         console.log(class_topic);
//         console.log(work); //final logic or command

        
//     }, 5000);
// }

function send_msg_to_bgscript(info)
  {
    console.log(info);
    chrome.runtime.sendMessage({ action: "sendAssignment", data: info});
  }
// Start observing
observer.observe(document.body, { 
  childList: true, 
  subtree: true 
});


