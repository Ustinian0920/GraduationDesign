<!--  -->
<template>
    <div class='main-div'>
        <el-row :gutter="20" class="title">
            <el-col :span="4">
                <div class="grid-content bg-purple header">组件</div>
            </el-col>
            <el-col :span="14">


                <div class="grid-content bg-purple header">
                    编辑
                </div>

            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple header">
                    <el-button :type="run_type" size="small" @click="run" :icon="run_icon">{{ run_str }}</el-button>
                    <el-button type="primary" size="small" @click="log" icon="el-icon-tickets">日志</el-button>
                    <el-button type="primary" size="small" @click="save" icon="el-icon-document-checked">保存</el-button>
                    <!-- <el-button type="primary" size="small" @click="drop" icon="el-icon-delete">删除</el-button> -->
                </div>
            </el-col>
        </el-row>
        <el-row :gutter="20" v-loading="loading" element-loading-background="rgba(0, 0, 0, 0.8)" element-loading-spinner="el-icon-loading" element-loading-text="工作流运行中">
            <el-col :span="4">
                <div class="left-content bg-purple main">


                    <div class="pre-div" v-for="i in cardList" :key="i.card_id">
                        <div class="pre-commponent">
                            {{ i.card_name }}
                        </div>
                        <el-button @click="addActor(i)" style="margin-bottom:10px" type="primary" size="mini"
                            icon="el-icon-right" circle></el-button>
                    </div>

                    <!-- <div class="pre-commponent" v-for="i in 6" :key="i">
                        组件{{ i }}
                    </div>
                    <div class="pre-commponent">
                        结束
                    </div> -->
                </div>
            </el-col>
            <el-col :span="14">
                <div class="middle-content bg-purple main">

                    <!-- <el-tree  class="flow-tree" :data="TreeData" :default-expanded-keys="[2, 3]"
                        :default-checked-keys="[5]" :props="defaultProps" default-expand-all draggable="true"
                        :allow-drop="allowDrop" @node-drag-start="nodeDragStart">
                    </el-tree> -->

                    <super-flow ref="superFlow" :node-list="nodeList" :link-list="linkList" :graph-menu="graphMenu"
                        :node-menu="nodeMenu" :link-menu="linkMenu" :link-base-style="linkBaseStyle"
                        :link-style="linkStyle" :link-desc="linkDesc" :graph-selected="graphSelected">
                        <template v-slot:node="{ meta }">
                            <div @mouseup="nodeMouseUp"
                                style="line-height: 30px;text-align: center;color: white;background: #3a8ee6"
                                class="flow-node ellipsis">
                                {{ meta.name }}
                            </div>
                        </template>
                    </super-flow>




                </div>
            </el-col>
            <el-col :span="6">
                <div class="right-content bg-purple main">

                    <el-form ref="form" :model="form" label-width="80px">
                        <el-form-item label="SHOT:">
                            <el-input v-model="shot"></el-input>
                        </el-form-item>
                        <el-form-item label="提交节点:">
                            <el-select v-model="form.node">
                                <el-option label="cluster01" value="cluster01"></el-option>
                                <el-option label="cluster02" value="cluster02"></el-option>
                            </el-select>
                        </el-form-item>

                        <el-form-item label="优先队列:">
                            <el-switch v-model="form.queue"></el-switch>
                        </el-form-item>

                        <el-form-item label="作业简介:">
                            <el-input type="textarea" v-model="form.introduction"></el-input>
                        </el-form-item>

                    </el-form>


                </div>
            </el-col>
        </el-row>


        <el-dialog title="运行日志" :visible.sync="logVisible">
            <el-input 
                id="textarea_id"
                type="textarea"
                :rows="20"
                placeholder="请输入内容"
                v-model="log_text" 
                readonly="">
            </el-input>
        </el-dialog>

        <el-drawer ref="navDrawer" :title="currentNode.meta.name" :visible.sync="drawer" :before-close="handleClose" >
            <el-form label-width="80px">

                <el-col v-for="i in Object.keys(cardParamList)" :key="i">
                    <el-form-item :label="i" >
                        <el-input :value="cardParamList[i]" @input="onInput()"></el-input>
                    </el-form-item>
                </el-col>
                
                <el-form-item>
                    <el-button type="primary" @click="save_params">保存</el-button>
                    <el-button @click="cancel_params">取消</el-button>
                </el-form-item>

            </el-form>
        </el-drawer>
    </div>






</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import SuperFlow from 'vue-super-flow'
import 'vue-super-flow/lib/index.css'
import { editStruct,editRun,editLog,editSave,cardList,getFlowSubParams,updateFlowSubParams } from '@/api/index'
const drawerType = {
    node: 0,
    link: 1
}


export default {
    //组件名称
    name: 'Main2',
    //父组件传递值
    props: {
    },
    //import引入的组件需要注入到对象中才能使用
    components: {
        SuperFlow
    },
    data() {
        //这里存放数据
        return {
            line:1000,
            log_text:"123123123123123",
            loading:false,
            shot:127,
            flow_id : 0,
            // 运行按钮的值
            run_icon: "el-icon-video-play",
            run_str: "运行",
            run_type: "primary",

            logVisible: false,

            drawer: false,

            graphSelected: true,

            form: {
                id: "123456",
                node: "cluster01",
                queue: true,
                introduction: ""
            },
            
            // 左侧竖排组件列表
            cardList:[],
            // 点击编辑组件的组件参数列表
            cardParamList:{},
            // 当前选中的组件
            currentNode:{"meta":{"name":"tem"}},

            linkList: [],

            nodeList: [
                {
                    id: 'nodeStart',
                    width: 120,
                    height: 30,
                    coordinate: [
                        300,
                        10
                    ],
                    meta: {
                        lable: '',
                        name: '开始',
                        algoId: '0',
                        nextNodeId: [],
                        nextAlgoId: []
                    }
                },
                {
                    id: 'nodeEnd',
                    width: 120,
                    height: 30,
                    coordinate: [
                        300,
                        400
                    ],
                    meta: {
                        lable: '',
                        name: '结束',
                        algoId: '3',
                        nextNodeId: [],
                        nextAlgoId: []
                    }
                },
            ],

            drawerConf: {
                title: '',
                visible: false,
                type: null,
                info: null,
                open: (type, info) => {
                    const conf = this.drawerConf
                    conf.visible = true
                    conf.type = type
                    conf.info = info
                    if (conf.type === drawerType.node) {
                        conf.title = '算法详情'
                        if (this.$refs.nodeSetting) this.$refs.nodeSetting.resetFields()
                        this.$set(this.nodeSetting, 'name', info.meta.name)
                        this.$set(this.nodeSetting, 'desc', info.meta.desc)
                        this.nodeSetting.Items = []
                    }
                },
                cancel: () => {
                    this.drawerConf.visible = false
                    if (this.drawerConf.type === drawerType.node) {
                        this.$refs.nodeSetting.clearValidate()
                    } else {
                        this.$refs.linkSetting.clearValidate()
                    }
                }

            },

            linkSetting: {
                desc: ''
            },

            nodeSetting: {
                name: '',
                desc: '',
                ExeName: '',
                Items: []
            },

            dragConf: {
                isDown: false,
                isMove: false,
                offsetTop: 0,
                offsetLeft: 0,
                clientX: 0,
                clientY: 0,
                ele: null,
                info: null
            },

            data: [],

            defaultProps: {
                children: 'children',
                label: 'label'
            },

            graphMenu: [
                [
                    {
                        label: '全选',
                        selected: graph => {
                            graph.selectAll()
                        }
                    }
                ],
                [
                    {
                        label: 'console.log json',
                        selected: (graph) => {
                            console.log(JSON.stringify(graph.toJSON(), null, 2))
                        }
                    }
                ]
            ],

            // node 右键菜单配置
            nodeMenu: [
                [
                    {
                        label: '删除组件',
                        selected: node => {
                            node.remove()
                        }
                    },
                    {
                        label: '编辑参数',
                        selected: node => {
                           
                            console.log(node)
                            this.currentNode = node
                            getFlowSubParams({
                                flow_id:this.flow_id,
                                private_sub_id:node.id,
                                public_sub_id:node.meta.label
                            }).then(res=>{
                                console.log(res)
                                this.cardParamList=res.data
                                console.log(this.cardParamList)
                            })
                            
                    
                            this.drawer = true;
                        }
                    }
                ]
            ],

            linkMenu: [
                [
                    {
                        label: '删除',
                        selected: link => {
                            link.remove()
                        }
                    },
                    {
                        label: '编辑',
                        selected: link => {
                            this.drawerConf.open(drawerType.link, link)
                        }
                    }
                ]
            ],

            linkBaseStyle: {
                color: '#000', // line 颜色
                hover: '#666666', // line hover 的颜色
                textColor: '#666666', // line 描述文字颜色
                textHover: '#FF0000', // line 描述文字 hover 颜色
                font: '14px Arial', // line 描述文字 字体设置 参考 canvas font
                dotted: false, // 是否是虚线
                lineDash: [4, 4], // 虚线时生效
                background: 'rgba(255,255,255,0.6)' // 描述文字背景色
            },

            fontList: [
                '14px Arial',
                'italic small-caps bold 12px arial'
            ],

            nodeSub: null

        };
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {},
    //方法集合
    methods: {
        run() {
        
            this.line = 1000
            window.timer = setInterval(()=>{
                setTimeout(()=>{
                    editLog({line:this.line}).then(res=>{
                        this.log_text = res.data
                        this.line = 1000+this.line
                    })
                },1000)
            },1000)
            
            
            this.loading = true
            this.run_icon === "el-icon-video-play" ? this.run_icon = "el-icon-video-pause" : this.run_icon = "el-icon-video-play",
                this.run_str === "运行" ? this.run_str = "停止" : this.run_str = "运行"
            this.run_type === "primary" ? this.run_type = "danger" : this.run_type = "primary"
            if(this.run_type=="danger"){
                editRun({
                    shot:this.shot,
                }).then(res=>{
                    this.run_icon = "el-icon-video-play" 
                    this.run_type = "primary"
                    this.run_str = "运行"
                    this.loading = false
                    this.$message({
                        message: '运行完成',
                        type: 'success'
                    });
                    clearInterval(timer)
                })
            }
            
        },
        log() {
            this.logVisible = true
        },
        save() {
            console.log(JSON.stringify(this.$refs.superFlow.graph.toJSON(), null, 2))
            
            editSave({
                id:this.flow_id,
                data:JSON.stringify(this.$refs.superFlow.graph.toJSON(), null, 2),
            }).then(res=>{
                console.log(res)
            })
            this.$message({
                message: '保存成功',
                type: 'success',
                duration: 2000
            });
        },
        
        drop() {

        },

        getCardList(){
            cardList({
                card_type:1,
            }).then(res=>{
                console.log(res)
                this.cardList=res.data
            })
        },

   



        // 点击->按钮
        addActor(item) {
            var node = {
                id: item.card_id,
                width: 120,
                height: 30,
                coordinate: [
                    10,
                    10 + (item.index) * 40
                ],
                meta: {
                    lable: '',
                    name: item.card_name,
                    algoId: item.card_id,
                    nextNodeId: [],
                    nextAlgoId: []
                }
            }
            this.$refs.superFlow.graph.addNode(node)
        },


        handleClose(done) {
            // this.$confirm('确认关闭？')
            //     .then(_ => {
                    done();
            //     })
            //     .catch(_ => { });
        },

        
        onInput() {
            this.$forceUpdate();
        },

        save_params(){
            updateFlowSubParams({
                flow_id:this.flow_id,
                sub_id:this.currentNode.meta.id,
                params_dic:this.cardParamList
            }).then(res=>{
                console.log(res)
                this.$refs.navDrawer.closeDrawer();
                this.$message({
                    message: '保存成功',
                    type: 'success'
                });
            })
        },

        cancel_params(){
            this.$refs.navDrawer.closeDrawer();
        },


        // 拖拽控制
        allowDrop(moveNode, inNode, type) {
            //限制树节点拖拽后是否可以放置在当前位置，值为true时可以，为false时不可以
            return false
        },

        nodeDragStart(node, event) {
            const {
                clientX,
                clientY,
                currentTarget
            } = event

            const {
                top,
                left
            } = event.currentTarget.getBoundingClientRect()

            const conf = this.dragConf
            const ele = currentTarget.cloneNode(true)

            Object.assign(this.dragConf, {
                offsetLeft: clientX - left,
                offsetTop: clientY - top,
                clientX: clientX,
                clientY: clientY,
                info: node.data.value(),
                ele,
                isDown: true
            })

            ele.style.position = 'fixed'
            ele.style.margin = '0'
            ele.style.top = clientY - conf.offsetTop + 'px'
            ele.style.left = clientX - conf.offsetLeft + 'px'

            this.$el.appendChild(this.dragConf.ele)
        },

        linkStyle(link) {
            if (link.meta && link.meta.desc === '1') {
                return {
                    color: 'red',
                    hover: '#FF00FF',
                    dotted: true
                }
            } else {
                return {}
            }
        },

        linkDesc(link) {
            return link.meta ? link.meta.desc : ''
        },

        nodeMouseUp(evt) {
            evt.preventDefault()
        },

        docMousemove({ clientX, clientY }) {
            const conf = this.dragConf

            if (conf.isMove) {
                conf.ele.style.top = clientY - conf.offsetTop + 'px'
                conf.ele.style.left = clientX - conf.offsetLeft + 'px'
            } else if (conf.isDown) {
                // 鼠标移动量大于 5 时 移动状态生效
                conf.isMove =
                    Math.abs(clientX - conf.clientX) > 5 ||
                    Math.abs(clientY - conf.clientY) > 5
            }
        },

        docMouseup({ clientX, clientY }) {
            console.log('docMouseupgraph=', this.$refs.superFlow.graph)

            const conf = this.dragConf
            conf.isDown = false



            if (conf.isMove) {
                const {
                    top,
                    right,
                    bottom,
                    left
                } = this.$refs.flowContainer.getBoundingClientRect()
                console.log(top, right, bottom, left)
                // 判断鼠标是否进入 flow container
                if (
                    clientX > left &&
                    clientX < right &&
                    clientY > top &&
                    clientY < bottom
                ) {
                    console.log(1111111)
                    // 获取拖动元素左上角相对 super flow 区域原点坐标
                    const coordinate = this.$refs.superFlow.getMouseCoordinate(
                        clientX - conf.offsetLeft,
                        clientY - conf.offsetTop
                    )

                    // 添加节点
                    this.$refs.superFlow.addNode({
                        coordinate,
                        ...conf.info
                    })
                }

                conf.isMove = false
            }

            if (conf.ele) {
                conf.ele.remove()
                conf.ele = null
            }


        },

        docMousedown({ clientX, clientY }) {
            console.log(clientX, clientY)

        }
    },
    //生命周期 - 创建完成（可以访问当前this实例）
    created() {
        
    },
    //生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
        try{
            try{
                this.linkList = this.$route.params.res.data.linkList
            }catch(err){}
            this.nodeList = this.$route.params.res.data.nodeList
            this.flow_id = this.$route.params.flow_id
            console.log("初始化")
        }catch(err){}

        console.log(this.linkList)
        console.log(this.nodeList)
            

        this.getCardList()

        // document.addEventListener('mousemove', this.docMousemove)
        // document.addEventListener('mouseup', this.docMouseup)
        // document.addEventListener('mousedown', this.docMousedown)
        // this.$once('hook:beforeDestroy', () => {
        //     document.removeEventListener('mousemove', this.docMousemove)
        //     document.removeEventListener('mouseup', this.docMouseup)
        //     document.addEventListener('mousedown', this.docMousedown)
        // })
    },
    beforeCreate() { }, //生命周期 - 创建之前
    beforeMount() { }, //生命周期 - 挂载之前
    beforeUpdate() { }, //生命周期 - 更新之前
    updated() {
        try{
            this.$nextTick(() => {
                setTimeout(() => {
                    const textarea = document.getElementById('textarea_id');
                    textarea.scrollTop = textarea.scrollHeight;
                }, 1000)
            })
        }catch(err){console.log(err)}
            
     }, //生命周期 - 更新之后
    beforeDestroy() { }, //生命周期 - 销毁之前
    destroyed() { }, //生命周期 - 销毁完成
    activated() { }, //如果页面有keep-alive缓存功能，这个函数会触发
}
</script>
<style scoped>
/**scoped 表示样式只在当前组件有效*/

/deep/#textarea_id{
    color:white;
    background-color:black;
}

.el-row {
    margin-bottom: 10px;
    height: 90%;
}

/* .title {
    height: 10%;
} */

.bg-purple {
    background: #d3dce6;
}

.el-button {
    height: auto;
    margin-top: 10px;
    margin-left: 20px;
}

.header {
    height: 50px
}

.main {
    height: 695px
}


.pre-commponent {
    height: 30px;
    width: 120px;
    background-color: #3f90e3;
    margin-left: 5px;
    /* padding-top:10px; */
    color: white;

}

.pre-div {
    display: flex;
    align-items: center;
    margin-top: 10px;
    width: 180px;
    height: 30px;
    /* background-color: #fcfcfc; */
}

/* el-message el-message--success el-message-fade-enter-active el-message-fade-enter-to */
/* /deep/ .el-icon-video-play{
    font-size:14px;
} */
</style>