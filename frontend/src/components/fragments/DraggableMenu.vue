<template>
    <div
        v-bind:style="`top:${top}px;left:${left}px`"
        class="menu"
        ref="menuElem"
    >
        <div class="setting-list">
            <div
                class="drag-hook menu-upper-panel"
                v-on:mousedown.prevent="startDrag($event)"
                v-on:mouseup="endDrag"
            >
                <span>{{title}}</span>
                <button
                    v-on:click="onClose"
                    class="close-btn"
                >x</button>
            </div>

            <div class="setting-cont">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style>

    .setting-cont {
        width: 250px;
        height: 400px;
        overflow-y: scroll;
    }

    .menu {
        position: fixed;
        z-index: 1;
    }

    .menu-upper-panel {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: center;
        margin-bottom: 5px;
    }

    .drag-hook {
        width: 100%;
        background-color: lightgray;
        cursor: move;
    }

    .setting-list {
        background-color: whitesmoke;
        box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.2);
        border: 1.5px solid lightgray;
        overflow: hidden;
    }

    .close-btn {
        border-radius: 50%;
        background-color: gray;
        color: white;
        margin: 2px;
        border: none;
        outline: none;
        cursor: pointer;
    }
</style>

<script>
    export default {
        name: 'DraggableMenu',
        props: {
            title: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                top: 0,
                left: 0,
                start: {
                    x: 0,
                    y: 0
                },
                difference: {
                    x: 0,
                    y: 0
                },
                isDragging: false
            };
        },

        methods: {
            startDrag(ev) {
                this.isDragging = true;
                this.start = { x: ev.clientX, y: ev.clientY };

                let menuCoord = this.$refs.menuElem.getBoundingClientRect();

                this.difference = { 
                    x: menuCoord.left - this.start.x,
                    y: menuCoord.top - this.start.y
                };
            },

            moveDragged(ev) {
                if (!this.isDragging) return;
                let { clientHeight, clientWidth } = document.documentElement;
                let currPos = { x: ev.clientX, y: ev.clientY };
                let { width: menuW } = this.$refs.menuElem.getBoundingClientRect();
                
                let left = this.difference.x + currPos.x;
                let top = this.difference.y + currPos.y;
                
                if (left + menuW > clientWidth) {
                    left = clientWidth - menuW;
                }

                if (left < 0) left = 0; 
                if (top < 0) top = 0;

                this.left = left;
                this.top = top;
            },

            endDrag() {
                this.isDragging = false;
            },

            onClose() {
                this.$emit("close-menu");
            }
        },

        mounted() {
            document.addEventListener("mousemove", this.moveDragged);
            document.addEventListener("mouseleave", this.endDrag);
        },

        destroyed() {
            document.removeEventListener("mousemove", this.moveDragged);
        }
    };
</script>