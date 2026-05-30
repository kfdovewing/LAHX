
let doneTimer = null;

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      // Only process actual elements (ignore text/comments)
      if (node.nodeType === 1) {
        
        // 1. Check if the added node itself is the span
        if (node.matches('span.Grouping-styles__title')) {
          processElement(node);
        }

        // 2. IMPORTANT: Search for any target spans HIDDEN inside this new node
        const classes = node.querySelectorAll('span.Grouping-styles__title');
        classes.forEach(nested => processElement(nested));
        
        //NOTE: maybe put in own array bc it's your own tasks
        // const own_tasks = node.querySelectorAll('button.css-c4zpq1-view-link');
        // own_tasks.forEach(nested => processAssaignment(nested));

        const assignments = node.querySelectorAll('a.css-18p5viu-view-link');
        assignments.forEach(nested => processAssaignment(nested));

      }
    });
  });

});
// Helper function to handle the found elements
const class_topic = [];
const work = [];

function processElement(el) {
    clearTimeout(doneTimer);
    // console.log("Captured:", el.textContent.trim());
    //INFO: the . after el grabs the attributes of the node passed in
    class_topic.push(el.textContent.trim());
    timer();
//   console.log(doneTimer);
}

function processAssaignment(el) {
    clearTimeout(doneTimer);
    // console.log("Captured:", el.textContent.trim());
    work.push(el.lastElementChild.textContent.trim());
    timer();
//   console.log(doneTimer);
}

function timer(){
  doneTimer = setTimeout(() => {
        console.log("No new changes for 5 seconds. Disconnecting.");
        observer.disconnect();
        console.log(class_topic);
        console.log(work); //final logic or command

        chrome.runtime.sendMessage({ action: "sendArray", data: class_topic});

    }, 5000);
}


// Start observing
observer.observe(document.body, { 
  childList: true, 
  subtree: true 
});


