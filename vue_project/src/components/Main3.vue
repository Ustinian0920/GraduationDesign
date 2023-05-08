<!--  -->
<template>
    <div class='main-div'>
        <el-container>
            <el-container>

                <el-tabs v-model="graphActive" type="border-card" >
                    <el-tab-pane label="EFEIT" name="first">
                        <el-container>
                            <el-aside width="200px">
                                <el-tabs v-model="fileTypeActive" type="border-card" >
                                    <el-tab-pane label="模拟数据" name="mimetic">
                                        <div class="plot-aside">
                                            <el-tree :data="data_list_efit" v-loading="loading"  @node-click="clickEfit">
                                            </el-tree>
                                        </div>

                                    </el-tab-pane>
                                    <el-tab-pane label="实验数据" name="test">
                                        <div class="plot-aside">
                                            <el-tree :data="data_list_efit_follow" v-loading="loading"  @node-click="clickEfit">
                                            </el-tree>
                                        </div>
                                    </el-tab-pane>
                                </el-tabs>
                            </el-aside>
                            <el-main>
                                <div v-loading="loading" class="plot-main">
                                    <el-empty v-show="efitShowEmpty" description="描述文字"></el-empty>
                                    <img :src="imgEfit" >
                                </div>
                            </el-main>
                        </el-container>
                    </el-tab-pane>
                    <el-tab-pane label="叠加" name="second">
                        <el-container>
                            <el-aside width="200px">
                                <el-tabs v-model="fileTypeActive" type="border-card" >
                                    <el-tab-pane label="模拟数据" name="mimetic">
                                        <div class="plot-aside">
                                            <el-tree ref="tree" :data="data_list_overlay" :show-checkbox="true" v-loading="loading"  @check="clickOverlay">
                                            </el-tree>
                                        </div>
                                        
                                    </el-tab-pane>
                                    <el-tab-pane label="实验数据" name="test">
                                        <div class="plot-aside">
                                            <el-tree :data="data_list_overlay_follow" :show-checkbox="true" v-loading="loading" @check="clickOverlay">
                                            </el-tree>
                                        </div>
                                    </el-tab-pane>
                                </el-tabs>
                            </el-aside>
                            <el-main>
                                <div v-loading="loading" class="plot-main">
                                    <el-empty v-show="overlayShowEmpty" description="描述文字"></el-empty>
                                    <img :src="imgOverlay" alt="">
                                </div>
                            </el-main>
                        </el-container>
                    </el-tab-pane>
                    <el-tab-pane label="动画" name="third">
                        <el-container>
                            <el-aside width="200px">
                                <el-tabs v-model="fileTypeActive" type="border-card" >
                                    <el-tab-pane label="模拟数据" name="mimetic">
                                        <div class="plot-aside">
                                            <el-tree :data="data_list_gif" v-loading="loading"  @node-click="clickGif">
                                            </el-tree>
                                           
                                        </div>
                                    </el-tab-pane>
                                    <el-tab-pane label="实验数据" name="test">
                                        <div class="plot-aside">
                                            <el-tree :data="data_list_gif_follow" v-loading="loading"  @node-click="clickGif">
                                            </el-tree>
                                        </div>
                                    </el-tab-pane>
                                </el-tabs>
                            </el-aside>
                            <el-main>
                                <div v-loading="loading" class="plot-main">
                                    <el-empty v-show="gifShowEmpty" description="描述文字"></el-empty>
                                    <img :src="imgGif" alt="">
                                </div>
                            </el-main>
                        </el-container>
                    </el-tab-pane>
                    <el-tab-pane label="波形" name="fourth">
                        <el-container>
                            <el-aside width="200px">
                                <el-tabs v-model="fileTypeActive" type="border-card" >
                                    <el-tab-pane label="模拟数据" name="mimetic">
                                        <div class="plot-aside">
                                            <el-tree :data="data_list_waveform" show-checkbox v-loading="loading"  @check="clickWaveform">
                                            </el-tree>
                                
                                        </div>
                                    </el-tab-pane>
                                    <el-tab-pane label="实验数据" name="test">
                                        <div class="plot-aside">
                                            <el-tree :data="data_list_waveform_follow" show-checkbox v-loading="loading" @check="clickWaveform">
                                            </el-tree>
                                      
                                        </div>
                                    </el-tab-pane>
                                </el-tabs>
                            </el-aside>
                            <el-main>
                                <div v-loading="loading" class="plot-main">
                                    <el-empty v-show="waveformShowEmpty" description="描述文字"></el-empty>
                                    <img :src="imgWaveform" alt="">
                                </div>
                            </el-main>
                        </el-container>
                    </el-tab-pane>
                </el-tabs>

              
            </el-container>
        </el-container>
    </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

import { drawTree,drawSingle,drawOverlay,drawGif,drawWaveform } from '@/api/index';

export default {
    //组件名称
    name: 'Main3',
    //父组件传递值
    props: {
    },
    //import引入的组件需要注入到对象中才能使用
    components: {},
    data() {
        //这里存放数据
        return {
            loading:false,
            efitShowEmpty:true,
            overlayShowEmpty:true,
            gifShowEmpty:true,
            waveformShowEmpty:true,
            data_list_efit:[],
            data_list_efit_follow:[],
            data_list_overlay:[],
            data_list_overlay_follow:[],
            data_list_gif:[],
            data_list_gif_follow:[],
            data_list_waveform:[],
            data_list_waveform_follow:[],
            imgEfit:"",
            imgOverlay:"",
            imgGif:"",
            imgWaveform:"",
            waveformShotList:[],
            props: {
                label: 'name',
                children: 'zones'
            },
            graphActive: 'first',
            fileTypeActive:'mimetic'
        };
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {},
    //方法集合
    methods: {


        clickEfit(data,node,_){
            if(data.hasOwnProperty("children")){
                console.log("非叶子结点")

            }else{
                this.loading = true
                let is_follow = 1
                if (this.fileTypeActive=="mimetic"){is_follow=0}
                drawSingle({
                    shot:node.parent.data.label,
                    time:data.label,
                    is_follow:is_follow
                }).then(res=>{
                    this.imgEfit = "data:image/png;base64,"+res.data
                    this.loading = false
                    this.efitShowEmpty = false
                })

            }
            
        },

        clickOverlay(datas,status){
            this.loading = true
            let time_list = []
            for(let index in status.checkedNodes){
                console.log(index)
                time_list.push(status.checkedNodes[index].label)
            }
            drawOverlay({time_list:time_list}).then(res=>{
                this.imgOverlay = "data:image/png;base64,"+res.data
                this.loading = false
                this.overlayShowEmpty = false
            })
         
        },

        clickGif(data){
            this.loading = true
            drawGif({
                shot:data.label
            }).then(res=>{
                console.log(res)
                this.imgGif = res.data.url
                this.loading = false
                this.gifShowEmpty = false
            })

        },

        clickWaveform(data,status){
            this.loading = TransformStreamDefaultController
            let shot_list = []
            for(let index in status.checkedNodes){
                console.log(index)
                shot_list.push(status.checkedNodes[index].label)
            }
            this.waveformShotList = shot_list
            drawWaveform({
                shot_list:shot_list
            }).then(res=>{
                this.imgWaveform = "data:image/png;base64,"+res.data
                this.loading = false
                this.waveformShowEmpty = false
            })


        },

        getTree(plot_type,is_follow){
            drawTree({plot_type:plot_type,is_follow:is_follow}).then(res=>{
            
                if(res.return_code=="OK"){
                    if(plot_type == "efit"){
                        
                        if(is_follow==1){
                            this.data_list_efit_follow = res.data
                        }else{
                            this.data_list_efit = res.data
                        }
                        
                    }else if(plot_type=="overlay"){
                        if(is_follow==1){
                            this.data_list_overlay_follow = res.data
                        }else{
                            this.data_list_overlay = res.data
                        }

                    }else if(plot_type=="gif"){
                        if(is_follow==1){
                            this.data_list_gif_follow = res.data
                        }else{
                            this.data_list_gif = res.data
                        }

                    }else if(plot_type=="waveform"){
                        if(is_follow==1){
                            this.data_list_waveform_follow = res.data
                        }else{
                            this.data_list_waveform = res.data
                        }

                    }
                }
            })
        },
       

    },
    //生命周期 - 创建完成（可以访问当前this实例）
    created() {

    },
    //生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {  
        for(let plot_type in {efit:"efit",overlay:"overlay",gif:"gif",waveform:"waveform"}){
            for(let is_follow in [1,0]){
                this.getTree(plot_type,is_follow)
            }
        }
        
    },
    beforeCreate() { }, //生命周期 - 创建之前
    beforeMount() { }, //生命周期 - 挂载之前
    beforeUpdate() { }, //生命周期 - 更新之前
    updated() { }, //生命周期 - 更新之后
    beforeDestroy() { }, //生命周期 - 销毁之前
    destroyed() { }, //生命周期 - 销毁完成
    activated() { }, //如果页面有keep-alive缓存功能，这个函数会触发
}
</script>
<style  scoped>
/**scoped 表示样式只在当前组件有效*/
.el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
}

.el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
}

.plot-main{
    width:1380px;
    height:670px;
}

.plot-aside{
    height:480px;
}



 


 




</style>