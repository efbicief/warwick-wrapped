
class BlockResult{
    constructor(HtmlObject){
        this.htmlObject = HtmlObject;

        this.title = this.htmlObject.querySelectorAll(".block-title")[0];
        this.results=this.htmlObject.querySelectorAll(".block-results")[0];
        this.pages = this.results.querySelectorAll(".block-results-page");

        this.timePerPage =  [...this.pages].map(x=> 
            2*x.getElementsByClassName("result-group").length +
            4*x.querySelectorAll("img.result-group").length
            + 2);
        this.timePerPage[0] -=1

        this.size =
            2 // title
            + this.timePerPage.reduce((a,b)=> a+b,0) // total elements

        this.maxPosition=this.pages.length
        this.position=0;

    }
    /**
     * Time provided to animate the scene when using this.animate
     * 
     * typical values are 2s for title
     * 2s per key data point
     * 5s per long animation
     * @returns number of seconds 
     */
    get_time_animate() {
        return this.size;
    }

    /**
     * Scroll the current page right first if the capacity is available.
     * 
     * If no scroll  capacity is available return 1 and don't scroll else 
     * scroll and return 0
     * @returns 1 or 0 if the page has scrolled
     */
    scrollLeft(){
        if (this.position==1){
            this.position-=1;
            return 1
        }
        this.position-=1;
        this.results.scrollBy({
            top: 0,
            left: -10,
            behavior: "smooth",
          });
    }
    /**
     * Scroll the current page right first if the capacity is available.
     * 
     * If no scroll  capacity is available return 1 and don't scroll else 
     * scroll and return 0
     * @returns 1 or 0 if the page has scrolled
     */
    scrollRight(){ 
        if (this.position==0){
            this.position+=1;
        }
        if (this.position===this.maxPosition){
            return 1
        }
        this.position+=1;
        this.results.scrollBy({
            top: 0,
            left: 10,
            behavior: "smooth",
          });
    }

    nextPage(){
        if (this.position!=0){
            this.scrollRight()
        }else{
            this.position+=1
        }
        setTimeout(() => this.pages[this.position-1].setAttribute("data-shown","true"), 1000* (this.position!=1) );

        if (this.position==this.maxPosition){
            return;
        }
        setTimeout(() => this.nextPage.call(this), this.timePerPage[this.position-1]*1000);
    }

    /**
     * animate the current block result
     */
    animate(){
        this.title.setAttribute("data-shown","true");

        setTimeout(() => this.nextPage.call(this),3000);
    }
}


class mediaController{
    constructor(){
        //get data about structure of the pace
        this.blockPosition=0

        var resultBlocksHTML=
            document.getElementById("doc-body")
                .getElementsByClassName("result-block");

        this.resultBlocks = []
        for (var x of resultBlocksHTML){
            this.resultBlocks.push(new BlockResult(x))
        }
    }

    goDown(){
        if (this.blockPosition===this.resultBlocks.length+1){
            return 1
        }
        this.blockPosition+=1;
        document.getElementById("doc-body").scrollBy({
            top: 10,
            left: 0,
            behavior: "smooth",
          });
        return 0;
            }

    goUp(){
        if (this.blockPosition<=0){
            return 1
        }
        this.blockPosition-=1;
        document.getElementById("doc-body").scrollBy({
            top: -10,
            left: 0,
            behavior: "smooth",
          });
        return 0;
    }

    //slowly reduce audio volumne
    fadeOutAudio(){
        if (this.audio){
            if (this.audio.volume<=0.1){
                this.audio.pause();
                return
            }
            this.audio.volume-=0.1;
            setTimeout(()=>this.fadeOutAudio.call(this),100);
        }
    }

    nextBlock(){
        this.goDown();
        if (this.blockPosition===this.resultBlocks.length+1){
            document.getElementsByClassName("button-control-group")[0].setAttribute("data-shown","true");
            this.fadeOutAudio();
            return
        }
        this.resultBlocks[this.blockPosition-1].animate();
        setTimeout(() => this.nextBlock.call(this),this.resultBlocks[this.blockPosition-1].get_time_animate()*1000);
    }


    nextPage(){
        if (this.blockPosition== this.resultBlocks.length+1){
            return
        }
        if (this.blockPosition <=0){
            this.goDown();
            return
        }
        let result=this.resultBlocks[this.blockPosition-1].scrollRight()
        if (result ==1){
            this.goDown();
        }

    }
    previousPage(){
        if (this.blockPosition <=0){
            return;
        }
        if (this.blockPosition===this.resultBlocks.length+1){
            this.goUp();
            return;
        } 
        let result=this.resultBlocks[this.blockPosition-1].scrollLeft()
        if (result ==1){
            this.goUp();
        }
        
    }



    animate(){
        
        this.audio;

        if (! this.audio){
            this.audio = new Audio('static/images/upbeat-corporate.mp3');
        }
        if (this.audio.paused){
            this.audio.play()
        }

        this.nextBlock()
    }
}



var a=new mediaController()
// setTimeout( ()=>a.animate.call(a),2000);
var canClick = true;

function buttonUp(){
    if (canClick){
        a.previousPage()
        canClick=false;
        setTimeout( ()=> canClick=true ,500 );
    }
    
}
function buttonDown(){
    
    if (canClick){
        a.nextPage()
        canClick=false;
        setTimeout( ()=> canClick=true ,500 );
    }
}
