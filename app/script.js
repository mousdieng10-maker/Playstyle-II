import {find, findAll} from "./call.js";
import {hide, show} from "./utils.js";
const enterButton = find("#enterBtn");
const homeScreen = find("#homeScreen");
const leftSection = find(".left-section");
const generateScreen = find("#generateScreen");
const playingScreen = find("#playingScreen");

const LW= find("#LW");
const CAM= find("#CAM");
const RW= find("#RW");
const LM= find("#LM");
const CM= find("#CM");
const RM= find("#RM");
const ST= find("#ST");
const LB= find("#LB");
const CB= find("#CB");
const RB= find("#RB");
const GK= find("#GK");



hide(generateScreen);
hide(playingScreen);

enterButton.onclick = async function(){
    hide(homeScreen);
    show(generateScreen);
    const team = await window.pywebview.api.generate_team();
    for(const player of team){
        let position = player.position;
        if(position == "LW"){
            LW.innerHTML = player.name;

        }
        else if(position == "CAM"){
            CAM.textContent = player.name;
        }
        else if(position == "RW"){
            RW.textContent = player.name;
        }
        else if(position == "LM"){
            LM.textContent = player.name;
        }
        else if(position == "CM"){
            CM.textContent = player.name;
        }
        else if(position == "RM"){
            RM.textContent = player.name;
        }
        else if(position == "ST"){
            ST.textContent = player.name;
        }
        else if(position == "LB"){
            LB.textContent = player.name;
        }
        else if(position == "CB"){
            CB.textContent = player.name;
        }
        else if(position == "RB"){
            RB.textContent = player.name;
        }
        else if(position == "GK"){
            GK.textContent = player.name;
        }
    }
    document.body.style.display = "block"; 
    hide(generateScreen);
    show(playingScreen);
}