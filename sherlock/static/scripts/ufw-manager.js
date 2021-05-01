
//import data from context

const dataNode = document.getElementById("data");

dataNode.dataset.context = dataNode.dataset.context.replaceAll("'", "\"")

const data = JSON.parse(dataNode.dataset.context);

console.log(data);

//select rules from object

rulesFromData = Object.values(data['rules']);

console.log(rulesFromData);

//create array to store rule numbers to ensure deletes are feeded correctly

var ruleCodeArray = [];


ruleDeleter = function(ruleNumber, ruleArray){
    console.log("incoming rule number: " + ruleNumber);
    //get actual rule number from model array
    console.log("position of rule: " + (ruleArray.indexOf(ruleNumber)+1))
    adjustedRuleNum = ruleArray.indexOf(ruleNumber)*1+1;
    //remove rule from array
    ruleArray.splice(ruleNumber-1,1);
    console.log(ruleArray);
    scriptURL = '/ufw-delete-rule/' + adjustedRuleNum + '/';

    //hit URL in hidden div to interface with firewall via python
    $(function(scriptURL) {
         console.log("hit " + scriptURL)
         $('#urlLoader').load(scriptURL);
    }(scriptURL));

}

createRuleDivs = function(rules, ruleArray){
    console.log(rules.length);

    //loop through index of rules from ufw firewall

    for (i=0;i<rules.length;i++){

        //adjust rule data from array
        var ruleNum = i+1;
        var ruleName = "rule" + ruleNum;

        //record rule in rule array
        ruleArray.push(ruleNum.toString())

        //create rule list item
        ruleListItem = document.createElement("li");
        ruleListItem.className = "ruleListItem";
        ruleListItem.innerHTML = rules[i];
        ruleListItem.id = ruleName;

        //add close button to rule list item
        closeButton = document.createElement("span");
        closeButton.className = "close";
        closeButton.innerHTML = "X";
        closeButton.addEventListener("click", function() {
            this.parentElement.style.display = 'none';
            parID = this.parentElement.id;
            ruleNum = parID.substring(4,parID.length);
            ruleDeleter(ruleNum, ruleArray)
            console.log(ruleNum);

        });

        //glue everything together
        ruleListItem.appendChild(closeButton);
        console.log("Appending " + ruleListItem);
        document.getElementById("rulelist").appendChild(ruleListItem);

    }
}

//load rules into list items

createRuleDivs(rulesFromData, ruleCodeArray );

console.log(ruleCodeArray);