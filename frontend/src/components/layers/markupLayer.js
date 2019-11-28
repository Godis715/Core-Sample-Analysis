function drawMultilineText(ctx, lines, x, y, settings) {
    ctx.font = `${settings.fontSize}px ${settings.font}`;

    let top = y;
    lines.forEach(l => {
        ctx.fillText(l, x, top + settings.fontSize);
        top += settings.fontSize + settings.textMargin;
    });
}

function getMultilineHeight(lines, settings) {
    return lines.length * (settings.fontSize + settings.textMargin) - settings.textMargin;
}

export const MarkupLayer = {
    defaultSettings: Object.freeze({
        fontColor: "black",
        lineColor: "black",
        fontSize: 20,
        hideOverflow: true,
        textMargin: 5,
        font: "monospace",
        showText: true
    }),

    draw(canvas, data, width, res, settings) {
        let layers = data;
        let ctx = canvas.getContext("2d");

        ctx.fillStyle = settings.fontColor;
        ctx.strokeStyle = settings.lineColor;

        for (let i = 0; i < layers.length; ++i) {
            let topPx = layers[i].top * res;
            ctx.beginPath();
            ctx.moveTo(0, topPx);
            ctx.lineTo(width, topPx);
            ctx.stroke();
        }
        
        if (!settings.showText) return;
        for (let i = 0; i < layers.length; ++i) {
            let topPx = layers[i].top * res;
            let layerHeight = (layers[i].bottom - layers[i].top) * res;

            let multiline = []
            for (let cl in layers[i].classes) {
                multiline.push(`${cl}: ${layers[i].classes[cl]}`);
            }

            if (settings.hideOverflow) {
                let textHeight = getMultilineHeight(multiline, settings);
                if (textHeight < layerHeight) {
                    drawMultilineText(ctx, multiline, 0, topPx, settings);
                }
            } else {
                drawMultilineText(ctx, multiline, 0, topPx, settings);
            }

        }
    },

    mergeMarkup(markup) {
        let merged = [];
        for (let type in markup) {
            markup[type].forEach(lay => {
                merged.push({
                    type: type,
                    ...lay
                });
            });
        }
        return merged;
    },
    
    single2multiTypeLayers(layers) {
        layers.sort((l1, l2) => {
            return l1.top - l2.top;
        });
        let upperLayers = layers.filter(l => l.top === 0);
        let currClasses = {};

        upperLayers.forEach(l => currClasses[l.type] = l.class);

        let multi = [];
        multi.push({
            classes: { ...currClasses },
            top: 0
        });
        for (let i = upperLayers.length; i < layers.length; ++i) {
            let type = layers[i].type;
            currClasses[type] = layers[i].class;

            if (multi[multi.length-1].top !== layers[i].top) {
                multi[multi.length-1].bottom = layers[i].top;
                multi.push({
                    classes: { ...currClasses },
                    top: layers[i].top
                });
            } else {
                multi[multi.length-1].classes[type] = layers[i].class
            }
        }
        multi[multi.length-1].bottom = layers[layers.length-1].bottom;
        return multi;
    }
};