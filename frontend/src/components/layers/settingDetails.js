export const SettingDetails = Object.freeze({
    fragmentsWidthFit: {
        type: "radio",
        title: "Image width fit",
        options: [
            {
                name: "align left",
                value: "alignLeft"
            },
            {
                name: "align right",
                value: "alignRight"
            },
            {
                name: "stretch",
                value: "stretch"
            }
        ]
    },

    lineColor: {
        title: "Line color",
        type: "radio",
        options: [
            {
                name: "black",
                value: "black"
            },
            {
                name: "white",
                value: "white"
            },
            {
                name: "red",
                value: "red"
            },
            {
                name: "green",
                value: "green"
            },
            {
                name: "blue",
                value: "blue"
            },
        ]
    },

    fontColor: {
        title: "Font color",
        type: "radio",
        options: [
            {
                name: "black",
                value: "black"
            },
            {
                name: "white",
                value: "white"
            },
            {
                name: "red",
                value: "red"
            },
            {
                name: "green",
                value: "green"
            },
            {
                name: "blue",
                value: "blue"
            },
        ]
    },

    showText: {
        title: "Show text",
        type: "checkbox",
        default: true
    }
});