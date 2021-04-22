/* Get all elements with class="close" */
var closebtns = document.getElementsByClassName("close");
var i;
console.log("running closebtns")

    const dataNode = document.getElementById("data");

    dataNode.dataset.context = dataNode.dataset.context.replaceAll("'", "\"")

    const data = JSON.parse(dataNode.dataset.context);

console.log(data);
rules = Object.values(data['rules']);
console.log(rules);

var ruleArray = [];


/*Loop through the elements, and hide the parent, when clicked on
for (i = 0; i < closebtns.length; i++) {
    closebtns[i].addEventListener("click", function() {
        this.parentElement.style.display = 'none';
    });
}*/

ruleDeleter = function(ruleNumber){
    console.log("incoming rule number: " + ruleNumber);
    //get actual rule number from model array
    console.log("position of rule: " + (ruleArray.indexOf(ruleNumber)+1))
    adjustedRuleNum = ruleArray.indexOf(ruleNumber)*1+1;
    //remove rule from array
    ruleArray.splice(ruleNumber-1,1);
    console.log(ruleArray);
    scriptURL = '/ufw-delete-rule/' + adjustedRuleNum + '/';



    $(function(scriptURL) {
         console.log("hit " + scriptURL)
         $('#urlLoader').load(scriptURL);
    }(scriptURL));

}

createRuleDivs = function(rules){
    console.log(rules.length);
    for (i=0;i<rules.length;i++){
        var ruleNum = i+1;
        var ruleName = "rule" + ruleNum;

        ruleArray.push(ruleNum.toString())

        ruleListItem = document.createElement("li");
        ruleListItem.className = "ruleListItem";
        ruleListItem.innerHTML = rules[i];
        ruleListItem.id = ruleName;

        closeButton = document.createElement("span");
        closeButton.className = "close";
        closeButton.innerHTML = "X";
        closeButton.addEventListener("click", function() {
            this.parentElement.style.display = 'none';
            parID = this.parentElement.id;
            _ruleNum = parID.substring(4,parID.length);
            ruleDeleter(_ruleNum )
            console.log(_ruleNum);

        });

        ruleListItem.appendChild(closeButton);
        console.log("Appending " + ruleListItem);
        document.getElementById("rulelist").appendChild(ruleListItem);

    }
}

createRuleDivs(rules);
console.log(ruleArray);