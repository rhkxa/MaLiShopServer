# -*- coding: utf-8 -*-

##############################################################################
#
#
#
##############################################################################

from imp import reload
import basic
reload(basic)
from basic import public
DEBUG,CLIENT_NAME=public.DEBUG,public.CLIENT_NAME


if DEBUG == '1':    
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import hashlib , os , time , random

class cA007_dl(cBASE_DL):
    def init_data(self):

        self.GNL = ['','手机号码','昵称','类型','对象编号','名称','金额',
                    '使用条件','状态','订单号','领取时间','有效期','使用时间']

    #在子类中重新定义         
    def myInit(self):
        self.src = 'A007'
        pass

    def mRight(self):
            
        sql = u"""
            select g.id
                ,COALESCE(w.phone,'')
                ,w.name
                ,c.type
                ,c.refid
                ,c.name
                ,c.money
                ,c.use_money
                ,case when g.status=0 then '正常' else '已使用' end
                ,'需加订单号字段' --使用的订单号待处理
                ,g.ctime
                ,c.datestart ||'--'|| c.dateend----有效时间
                ,g.utime --使用时间 
            from get_coupon g
            left join wechat_mall_user w on w.id=g.wechat_user_id 
            left join coupon c on c.id=g.coupon_id
            where g.usr_id=%s and COALESCE(c.del_flag,0)=0
        """%self.usr_id

        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L

    def get_local_data(self , pk):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select c.id
                    
                    
                  
                  
            from menu_func c
            
            where  c.id=%s
           
        """ % pk
        if pk != '':
            L = self.db.fetch( sql )
        else:
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            danhao = time.strftime("%Y%m%d%H%M%S", timeArray)

            L['danhao']='cgdd'+danhao
        return L
    
    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}  
        pk = self.pk
        #dR={'R':'','MSG':'','isadd':''}
        dR={'R':'','MSG':''}

        
        
        #获取表单参数
        danhao=self.GP('danhao')#单号
        sp_name=self.GP('sp_name')#商品名
        sp_bh=self.GP('sp_bh')#商品编号
        sp_type=self.GP('sp_type')#商品类型
        candi=self.GP('candi')#产地
        num=self.GP('num')#数量
        dw=self.GP('dw')#单位
        gys_id = self.GP('gys_id')  # 供应商ID
        money=self.GP('money')#进货价格
        in_date=self.GP('in_date')#进货时间
        beizhu=self.GP('beizhu')#备注



        
        data = {
                'danhao':danhao
                ,'sp_name':sp_name
                ,'sp_bh':sp_bh
                ,'sp_type':sp_type
                ,'candi':candi
                ,'num':num
                ,'dw':dw
                ,'gys_id':gys_id
                ,'money':money
                ,'in_date':in_date
                ,'beizhu':beizhu,
                'cid': self.usr_id,
                'ctime': self.getToday(6),
                'uid': self.usr_id,
                'utime': self.getToday(6)
        }


        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data.pop('cid')
            data.pop('ctime')
            #data.pop('random')

            self.db.update('cggl_cg' , data , " id = %s " % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data.pop('uid')
            data.pop('utime')
            
            self.db.insert('cggl_cg' , data)
            pk = self.db.insertid('cggl_cg_id')#这个的格式是表名_自增字段
            dR['isadd'] = 1
        #self.listdata_save(pk,danhao)
        dR['pk'] = pk
        
        return dR
