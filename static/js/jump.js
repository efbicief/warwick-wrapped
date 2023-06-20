
class BlockResult{
    constructor(htmlObject){
        this.htmlObject = htmlObject;
        this.basic= false
        if (!this.htmlObject.classList.contains("result-block")){
            this.basic=true
            return
        }

        this.title = this.htmlObject.querySelectorAll(".block-title")[0];
        this.results=this.htmlObject.querySelectorAll(".block-results")[0];
        this.pages = this.results.querySelectorAll(".block-results-page");

        this.pagePosition=0;

        this.page_width = this.pages[0].offsetWidth;
        this.total_width = htmlObject.offsetWidth;

        this.timePerPage =  [...this.pages].map(x=> 
            2*x.getElementsByClassName("result-group").length +
            4*x.querySelectorAll("img.result-group").length
            + 2);
        this.timePerPage[0] -=1

        this.size =
            2 // title
            + this.timePerPage.reduce((a,b)=> a+b,0) // total elements



    }

    getPagePosition(){
        this.blockPosition = Math.floor(this.htmlObject.scrollLeft/this.page_width);
    }

    hScrollToBlock(pageNumber){
        var scrollPosition = pageNumber*this.page_width;
        this.results.scrollTo({
            top: 0,
            left: scrollPosition,
            behavior: "smooth",
          });
    }

    scrollLeft(){
        this.getPagePosition();
        if (this.pagePosition>0){
            this.pagePosition-=1;
            this.hScrollToBlock(this.pagePosition);
        }
    }

    scrollRight(){
        this.getPagePosition();
        if (this.pagePosition<this.pages.length-1){
            this.pagePosition+=1;
            this.hScrollToBlock(this.pagePosition);
        }
    }

    canScrollLeft(){
        if (this.basic){
            return false
        }
        this.getPagePosition();
        return this.pagePosition>0
    }

    canScrollRight(){
        if (this.basic){
            return false
        }
        this.getPagePosition();
        return this.pagePosition<this.pages.length-1
    }

    get_time_animate() {
        return this.size;
    }

    hidePages(){
        if (this.basic){
            return
        }
        this.title.setAttribute("data-shown","false");
        this.pagePosition=0;
        this.hScrollToBlock(0);
        for (var x of this.pages){
            x.setAttribute("data-shown","false");
        }
    }

    animateLoop(callback){
        this.getPagePosition();
        if (this.canScrollRight()){
            this.scrollRight();
            this.pages[this.pagePosition].setAttribute("data-shown","true");
            setTimeout(()=>this.animateLoop(callback),1000*this.timePerPage[this.pagePosition])
        }else{
            callback()
        }
    }

    animateInitial(callback){
        this.pages[0].setAttribute("data-shown","true");
        setTimeout(()=>this.animateLoop(callback),1000*this.timePerPage[0])
    }

    animate(callback){
        if (this.basic){
            setTimeout(()=>callback(),1000)
            return
        }
        this.title.setAttribute("data-shown","true");
        setTimeout(()=>this.animateInitial(callback),2000);
    }



    resize(){
        if (this.basic){
            return
        }
        this.page_width = this.pages[0].offsetWidth;
        this.total_width = this.htmlObject.offsetWidth;
        this.hScrollToBlock(this.pagePosition);
    }
}


class mediaController{
    constructor(){
        //get data about structure of the pace
        this.blockPosition=0
        
        var resultBlocksHTML=
        document.getElementById("doc-body")
        .getElementsByClassName("block");
        
        this.element_height=resultBlocksHTML[0].offsetHeight;
        this.document_height=document.getElementById("doc-body").offsetHeight;

        this.resultBlocks = []
        for (var x of resultBlocksHTML){
            this.resultBlocks.push(new BlockResult(x))
        }

        this.audio = null;
    }
    
    get_Document_position(){
        this.blockPosition = Math.floor(document.getElementById("doc-body").scrollTop/this.element_height);
    }

    v_Scroll_to_block(blockNumber){
        var scrollPosition = blockNumber*this.element_height;
        document.getElementById("doc-body").scrollTo({
            top: scrollPosition,
            left: 0,
            behavior: "smooth",
          });
    }

    scrollUp(){
        this.get_Document_position();
        if (this.blockPosition>0){
            this.blockPosition-=1;
            this.v_Scroll_to_block(this.blockPosition);
        }
    }

    scrollDown(){
        this.get_Document_position();
        if (this.blockPosition<this.resultBlocks.length-1){
            this.blockPosition+=1;
            this.v_Scroll_to_block(this.blockPosition);
        } 
    }

    NextPage(){
        this.get_Document_position();
        if (this.resultBlocks[this.blockPosition].canScrollRight()){
            this.resultBlocks[this.blockPosition].scrollRight();
        }else{
            this.scrollDown();
        }
    }

    PreviousPage(){
        this.get_Document_position();
        if (this.resultBlocks[this.blockPosition].canScrollLeft()){
            this.resultBlocks[this.blockPosition].scrollLeft();
        }else{
            this.scrollUp();
        }
    }

    startAudio(){
        if (! this.audio){
            this.audio = new Audio('static/images/upbeat-corporate.mp3');
        }
        if (this.audio.paused){
            this.audio.play()
        }
    }

    fadeOutAudio(){
        if (this.audio){
            if (this.audio.volume<=0.1){
                this.audio.pause();
                this.audio=undefined;
                return
            }
            this.audio.volume-=0.1;
            setTimeout(()=>this.fadeOutAudio.call(this),100);
        }
    }

    startAnimation(){
        this.startAudio();
        document.getElementsByClassName("button-control-group")[0].setAttribute("data-shown","false");
        for (var x of this.resultBlocks){
            x.hidePages();
        }
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
          } else if (document.documentElement.webkitRequestFullscreen) { /* Safari */
            document.documentElement.webkitRequestFullscreen();
          } else if (document.documentElement.msRequestFullscreen) { /* IE11 */
            document.documentElement.msRequestFullscreen();
          }
        setTimeout(()=>this.animate.call(this),300);
    }

    endAnimation(){
        this.fadeOutAudio();
        document.getElementsByClassName("button-control-group")[0].setAttribute("data-shown","true");
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) { /* Safari */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE11 */
            document.msExitFullscreen();
        }
    }
    


    animate(){
        this.get_Document_position();
        if (this.blockPosition<this.resultBlocks.length-1){
            this.blockPosition+=1;
            this.v_Scroll_to_block(this.blockPosition);
            this.resultBlocks[this.blockPosition].animate(()=>this.animate.call(this));
        }else{
            this.endAnimation();
        }
    }

    resize(){
        this.element_height=document.getElementById("doc-body").getElementsByClassName("block")[0].offsetHeight;
        this.document_height=document.getElementById("doc-body").offsetHeight;
        this.v_Scroll_to_block(this.blockPosition);
        for (var x of this.resultBlocks){
            x.resize();
        }
    }
}

var a = undefined;
a = new mediaController()
addEventListener("resize", (event) => {a.resize();});
var canClick = true;

function startButtonClicked(){
    if (a){
        a.startAnimation();
    }else
    {
        a = new mediaController()
        a.startAnimation();
    }
}

function buttonUp(){
    a.PreviousPage();
}
function buttonDown(){
    a.NextPage();
}

//Keep (good)
function copyData(){
    navigator.clipboard.writeText(document.getElementById("share-link").value).then(()=>{})
}

function getSharable(){
    fetch("/api/share").then((response)=>{
        return response.json()
    }).then((data)=>{
        document.getElementById("share-link").value=data["link"]
    }).catch((err)=>{
        document.getElementById("share-link").value="Error"
    })
}
