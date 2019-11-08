export const ImageLayer = {
    settingsList: [
        "fragmentsWidthFit"
    ],

    draw(canvas, data, width, res, settings) {
        let frags = data;

        let ctx = canvas.getContext("2d");

        for (let i = 0; i < frags.length; ++i) {
            let img = new Image();
            img.src = "http:\\\\localhost:8000\\static\\core_sample\\" + frags[i].src;

            let dHeight = (frags[i].bottom - frags[i].top) * res;
            
            let dWidth =  frags[i].width * res * (frags[i].bottom - frags[i].top) / frags[i].height;

            let dy = frags[i].top * res;

            switch(settings.fragmentsWidthFit) {
                case "alignLeft":
                img.onload = () => ctx.drawImage(img, 0, dy, dWidth, dHeight);
                break;

                case "alignRight":
                img.onload = () => ctx.drawImage(img, width - dWidth, dy, width, dHeight);
                break;

                case "stretch":
                img.onload = () => ctx.drawImage(img, 0, dy, width, dHeight);
                break;
            }
        }
    }
};