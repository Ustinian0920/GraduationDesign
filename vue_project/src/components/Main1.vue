<!--  -->
<template>
    <div class='main-div'>
        <h2 align="left">我的组件</h2>
        <el-divider></el-divider>
        <div>
            <el-row :gutter="20">
                <el-col :span="4" v-for="a in privateCardSubList" :key="a.card_id">
                    <div class="grid-content bg-purple">
                        <el-card style="cursor:pointer" class="box-card" shadow="hover" @click.native="info(a.card_id,1)">
                            <div slot="header" class="clearfix">
                                <span>{{ a.card_name }}</span>
                                <el-dropdown placement="top" style="float: right;" trigger="hover">
                                    <el-button class="el-dropdown-link" style="float: right" type="text"
                                        icon="el-icon-more"></el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="edit_private(a.card_id,1)" >编辑信息</el-dropdown-item>
                                        <el-dropdown-item @click.native="edit_private_params(a.card_id,1)" >编辑参数</el-dropdown-item>
                                        <el-dropdown-item  @click.native="info(a.card_id,1)">详情</el-dropdown-item>
                                        <el-dropdown-item @click.native="delete_card(a.card_id,1)" >删除</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </div>
                            <div class="text item">
                                {{ a.card_describ.slice(0,10) }}...
                            </div>
                        </el-card>
                    </div>
                </el-col>
            </el-row>
        </div>


        <h2 align="left">我的工作流</h2>
        <el-divider></el-divider>
        <div>
            <el-row :gutter="20">
                <el-col :span="4" v-for="a in privateCardFlowList" :key="a.card_id">
                    <div class="grid-content bg-purple">
                        <el-card style="cursor:pointer" class="box-card" shadow="hover" @click.native="edit_workflow(a.card_id)">
                            <div slot="header" class="clearfix">
                                <span>{{ a.card_name }}</span>
                                <el-dropdown placement="top" style="float: right;" trigger="hover">
                                    <el-button class="el-dropdown-link" style="float: right" type="text"
                                        icon="el-icon-more"></el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="edit_private(a.card_id,2)" >编辑信息</el-dropdown-item>
                                        <el-dropdown-item  @click.native="info(a.card_id,2)">详情</el-dropdown-item>
                                        <el-dropdown-item @click.native="delete_card(a.card_id,2)">删除</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </div>
                            <div class="text item">
                                {{ a.card_describ.slice(0,10) }}...
                            </div>
                        </el-card>
                    </div>
                </el-col>
            </el-row>
        </div>

        <h2 align="left">公共的组件</h2>
        <el-divider></el-divider>
        <div>
            <el-row :gutter="20">
                <el-col :span="4" v-for="a in publicCardSubList" :key="a.card_id">
                    <div class="grid-content bg-purple">
                        <el-card style="cursor:default;" class="box-card" shadow="hover">
                            <div slot="header" class="clearfix">
                                <span>{{ a.card_name }}</span>

                                <el-dropdown placement="top" style="float: right;" trigger="hover">
                                    <el-button class="el-dropdown-link" style="float: right; padding: 3px 0" type="text"
                                        icon="el-icon-more"></el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item  @click.native="copy(a.card_id,3)">添加我的</el-dropdown-item>
                                        <el-dropdown-item  @click.native="info(a.card_id,3)">详情</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>


                            </div>
                            <div class="text item">
                                {{ a.card_describ.slice(0,10) }}...
                            </div>
                        </el-card>
                    </div>
                </el-col>
            </el-row>
        </div>

        <h2 align="left">公共的工作流</h2>
        <el-divider></el-divider>
        <div><el-row :gutter="20">
                <el-col :span="4" v-for="a in publicCardFlowList" :key="a.card_id">
                    <div class="grid-content bg-purple">
                        <el-card style="cursor:default" class="box-card" shadow="hover">
                            <div slot="header" class="clearfix">
                                <span>{{ a.card_name }}</span>
                                <el-dropdown placement="top" style="float: right;" trigger="hover">
                                    <el-button class="el-dropdown-link" style="float: right; padding: 3px 0" type="text"
                                        icon="el-icon-more"></el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item @click.native="copy(a.card_id,4)" >添加我的</el-dropdown-item>
                                        <el-dropdown-item @click.native="info(a.card_id,4)" >详情</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </div>
                            <div class="text item">
                                {{ a.card_describ.slice(0,10) }}...
                            </div>
                        </el-card>
                    </div>
                </el-col>
            </el-row></div>

        <div>
            <el-dialog ref="editSub" title="组件编辑" :visible.sync="editDialogFormVisible">
            <el-form label-width="80px">
                <el-form-item label="组件名称:" style="margin-top: 20px;">
                    <el-input v-model="current_card.name" ></el-input>
                </el-form-item>
                <el-form-item label="作者:" style="margin-top: 20px;">
                    <el-input v-model="current_card.author" ></el-input>
                </el-form-item>
                <el-form-item label="描述信息:" style="margin-top: 20px;">
                    <el-input v-model="current_card.describ" ></el-input>
                </el-form-item>
                <el-form-item label="装置依赖:" style="margin-top: 20px;">
                    <el-input v-model="current_card.equipment" ></el-input>
                </el-form-item>
                <el-form-item label="所属部门:" style="margin-top: 20px;">
                    <el-input v-model="current_card.department" ></el-input>
                </el-form-item>
                <el-form-item label="前置程序:" style="margin-top: 20px;">
                    <el-input v-model="current_card.program" ></el-input>
                </el-form-item>
                <el-form-item label="输出类型:" style="margin-top: 20px;">
                    <el-input v-model="current_card.output" ></el-input>
                </el-form-item>
                <el-form-item style="margin-top: 20px;">
                    <el-button >取 消</el-button>
                    <el-button @click="update_private()">确 定</el-button>
                </el-form-item>
            </el-form>
     
            
     
            </el-dialog>
        </div>

        <div>
            <el-dialog  title="参数编辑" :visible.sync="editParamsDialogFormVisible">
                <el-form label-width="80px">

                    <el-col v-for="i in Object.keys(current_card.parameters)" :key="i">
                        <el-form-item :label="i" style="margin-top: 20px;" >
                            <el-input :value="current_card.parameters[i]" ></el-input>
                        </el-form-item>
                    </el-col>

                    <el-form-item style="margin-top: 20px;">
                        <el-button >取 消</el-button>
                        <el-button @click="update_private_sub_prams()">确 定</el-button>
                    </el-form-item>

                </el-form>
            </el-dialog>
        </div>
        
        <div>
            <el-drawer title="我是标题" :visible.sync="infoDialogFormVisible" :with-header="false" :modal="false" >
                <div>
                    <el-descriptions :title="current_card.name" :column="1" border>
                        <el-descriptions-item label="作者">{{ current_card.author }}</el-descriptions-item>
                        <el-descriptions-item label="编程语言">
                            <el-tag size="small" style="margin-left: 3px;">matlab</el-tag>
                            <el-tag size="small" style="margin-left: 3px;">c++</el-tag>
                            <el-tag size="small" style="margin-left: 3px;">python</el-tag>
                        </el-descriptions-item>
                        <el-descriptions-item label="描述信息">{{ current_card.describ }}</el-descriptions-item>
                        <el-descriptions-item label="装置依赖">{{ current_card.equipment }}</el-descriptions-item>
                        <el-descriptions-item label="所属部门">{{ current_card.department }}</el-descriptions-item>
                        <el-descriptions-item label="前置程序">{{ current_card.program }}</el-descriptions-item>
                        <el-descriptions-item label="输出类型">{{ current_card.output }}</el-descriptions-item>
                        <el-descriptions-item label="更新时间">{{ current_card.update_time }}</el-descriptions-item>
                
                    </el-descriptions>
                </div>
            </el-drawer>
        </div>
    </div>

  
    
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import { editStruct,cardList,cardCopy,cardDelete,cardInfo,cardUpdate } from '@/api/index'
export default {
    //组件名称
    name: 'Main1',
    //父组件传递值
    props: {
    },
    //import引入的组件需要注入到对象中才能使用
    components: {},
    data() {
        //这里存放数据
        return {
            current_card : {
                id:"",
                name:"",
                describ:"",
                author:"",
                create_tiem:"",
                department:"",
                equipment:"",
                language:[],
                output:"",
                program:"",
                update_time:"",
                parameters:{}
            },
            editParamsDialogFormVisible:false,
            editDialogFormVisible : false,
            infoDialogFormVisible :false,
            privateCardSubList:[],
            privateCardFlowList:[],
            publicCardSubList:[],
            publicCardFlowList:[],
            
        };
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {},
    //方法集合
    methods: {
        edit_workflow(card_id){
            editStruct({
                card_id:card_id,
                card_type:2,
            }).then(res=>{
                console.log("res")
                console.log(res)
                this.$router.push({ name: "Menu2",params:{"res":res,"flow_id":card_id} })
            })
        },

        edit_private(card_id,card_type){
            cardInfo({
                card_id,card_type
            }).then(res=>{
                if(res.return_code=="OK"){
                    this.editDialogFormVisible = true
                    this.current_card = res.data.info
                }
            })
        },

        edit_private_params(card_id,card_type){
            cardInfo({
                card_id,card_type
            }).then(res=>{
                if(res.return_code=="OK"){
                    this.editParamsDialogFormVisible = true
                    this.current_card = res.data.info
                }
            })
        },


  

        update_private(){
            let tem_current_card = this.current_card
            cardUpdate({
                card_type:tem_current_card.card_type,
                card_id:tem_current_card.id,
                name:tem_current_card.name,
                describ:tem_current_card.describ,
                author:tem_current_card.author,
                equipment:tem_current_card.equipment,
                department:tem_current_card.department,
                program:tem_current_card.program,
                output:tem_current_card.output
            }).then(res=>{
                if(res.return_code=="OK"){
                   
                    this.editDialogFormVisible = false
                    cardList({
                        card_type:tem_current_card.card_type,
                        }).then(res=>{
                           
                            if (tem_current_card.card_type==1){
                                this.privateCardSubList = res.data
                            }else{
                                this.privateCardFlowList = res.data
                            }
                            
                    })
                    this.$message({
                        message: '保存成功',
                        type: 'success',
                        duration: 2000
                    });
                }
            })
        },

        update_private_sub_prams(){
            let tem_current_card = this.current_card
            cardUpdate({
                card_type:1,
                card_id:tem_current_card.id,
                parameters:tem_current_card.parameters
            }).then(res=>{
                if(res.return_code="OK"){
                    this.editParamsDialogFormVisible = false
                    cardList({
                        card_type:1
                    }).then(res=>{
                        this.privateCardSubList = res.data
                    })
                    this.$message({
                        message: '保存成功',
                        type: 'success',
                        duration: 2000
                    });
                }
            })
        },

        info(card_id,card_type){
            cardInfo({
                card_id,card_type
            }).then(res=>{
                if(res.return_code=="OK"){
                    this.infoDialogFormVisible = true
                    this.current_card = res.data.info
                }
            })
            
        },

        delete_card(card_id,card_type){
            cardDelete({
                card_id:card_id,
                card_type:card_type,
            }).then(res=>{
                if(res.return_code=="OK"){
                   
                    cardList({
                        card_type:card_type,
                        }).then(res=>{
                            if (card_type==1){
                                this.privateCardSubList = res.data
                            }else{
                                this.privateCardFlowList = res.data
                            }
                            
                    })
                }
            })
        },

        copy(card_id,card_type){
            cardCopy({
                card_id:card_id,
                card_type:card_type,
            }).then(res=>{
                if(res.return_code=="OK"){
                    cardList({
                        card_type:card_type-2,
                        }).then(res=>{
                            if (card_type==3){
                                this.privateCardSubList = res.data
                            }else{
                                this.privateCardFlowList = res.data
                            }
                            
                    })
                }
            })
        },

      

        

        





        get_private_sub_list(){
            res = cardList({card_type:1})
            this.privateCardSubList = res.data
            return res.data
        },

        get_private_flow_list(){
            res = cardList({card_type:2})
            this.privateCardFlowList = res.data
            return res.data
        },

        get_public_sub_list(){
            res = cardList({card_type:3})
            this.publicCardSubList = res.data
            return res.data
        },

        get_public_flow_list(){
            res = cardList({card_type:4})
            this.publicCardFlowList = res.data
            return res.data
        },
    },
    //生命周期 - 创建完成（可以访问当前this实例）
    created() {
        cardList({
            card_type:1,
            }).then(res=>{
                this.privateCardSubList = res.data
        })

        cardList({
            card_type:2,
            }).then(res=>{
                console.log("我的工作流")
                console.log(res.data)
                this.privateCardFlowList = res.data
        })

        cardList({
            card_type:3,
            }).then(res=>{
                this.publicCardSubList = res.data
        })

        cardList({
            card_type:4,
            }).then(res=>{
    
                this.publicCardFlowList = res.data
        })

    },
    //生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
        
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
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    height: auto;
}

h2 {
    margin-top: 20px;
    margin-bottom: 20px;
}

/deep/ .el-icon-more {
    margin-top: 0px;
    font-size: 20px;
}
.el-dropdown-item{
    margin-left:15px;
    margin-right:15px;
}

</style>