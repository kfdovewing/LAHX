


let queue = [];
let doneTimer = null;
const processedPairs = new Set();

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === 'childList' && mutation.addedNodes.length > 0){
      mutation.addedNodes.forEach((node) => {
    //   // Only process actual elements (ignore text/comments)
        if (node.nodeType === Node.ELEMENT_NODE) {
        
        // 1. Check if the added node itself is the span
        if (node.matches('span.Grouping-styles__title')) {
          // className = node.textContent.trim()
          // console.log(className);
          processElement(node);
        }

        const group = node.querySelectorAll('div.Grouping-styles__root.Grouping-styles__medium.planner-grouping');
        group.forEach((nested) => {
          const titleSpan = nested.querySelector('span.Grouping-styles__title');

          const assign = nested.querySelector('a.css-18p5viu-view-link span:nth-of-type(2)');

          if (titleSpan && assign) {
            const className = titleSpan.textContent.trim();
            const assignmentName = assign.textContent.trim();
            const pairKey = `${className} -> ${assignmentName}`;

            if (!processedPairs.has(pairKey)) {
              processedPairs.add(pairKey);
              
              processAssaignment(className, assignmentName);
              timer()
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
// Helper function to handle the found elements
function processAssaignment(classes, task) {
    full_task = classes + ": " + task;
    queue.push(full_task);
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
  subtree: true 
});


