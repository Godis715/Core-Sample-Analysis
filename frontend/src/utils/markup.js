export default markup = {
    /**
     * 
     * @param markup { layerType1: array of { top: ..., bottom: ..., class: ... }, ... }
     * 
     * @return array of { type: layerType1, top: ..., bottom: ..., class: ... }
     * 
     * function converts markup object, where types of layers are keys and layers are values
     * to single array of layers, where 'type' is a field of each layer
     */
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
    
    /**
     * 
     * @param layers array of { type: layerType1, top: ..., bottom: ..., class: ... }
     * 
     * @return array of { classes: { layerType1: className1, ... }, top: ..., bottom: ... }
     * 
     * function convert array of layers of different types to array of layers 
     * with multiple type, which is contained in 'classes' as dictionary { layerType1: className1, ... }
     */
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