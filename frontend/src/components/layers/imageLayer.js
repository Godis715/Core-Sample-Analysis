export const ImageLayer = {
    defaultSettings: Object.freeze({
        fragmentsWidthFit: "stretch"
    }),

    draw(canvas, data, width, res, settings) {
        function promisifyDrawImage(ctx, img, x1, y1, x2, y2) {
            return new Promise((res, rej) => {
                img.onload = () => {
                    ctx.drawImage(img, x1, y1, x2, y2);
                    res();
                };
            });
        }

        let frags = data;
        let ctx = canvas.getContext("2d");
        let promises = [];

        for (let i = 0; i < frags.length; ++i) {
            let img = new Image();
            img.src = "http:\\\\localhost:8000\\static\\core_sample\\" + frags[i].src;

            let dHeight = (frags[i].bottom - frags[i].top) * res;
            let dWidth =  frags[i].width * res * (frags[i].bottom - frags[i].top) / frags[i].height;
            let dy = frags[i].top * res;

            switch(settings.fragmentsWidthFit) {
                case "alignLeft":
                promises.push( promisifyDrawImage(ctx, img, 0, dy, dWidth, dHeight) );
                break;

                case "alignRight":
                promises.push( promisifyDrawImage(ctx, img, width - dWidth, dy, width, dHeight) );
                break;

                case "stretch":
                promises.push( promisifyDrawImage(ctx, img, 0, dy, width, dHeight) );
                break;
            }
        }

        return Promise.all(promises);
    }
};