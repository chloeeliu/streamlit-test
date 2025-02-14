import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

#load file
df_log=pd.read_excel('log.xlsx')
##处理时间字段--日期
df_log['date']=df_log['操作时间'].astype(str).str[:10]
##处理时间字段--月份
df_log['month']=df_log['操作时间'].astype(str).str[:7]

#define aggregate log data with certain label
def log_stat(typ,log_label='all'):
    if log_label == 'all':
        
        if typ == 'day': 
            df_stat_day=df_log.groupby(['date']).agg({'操作人':['nunique','count'] }).reset_index()
            df_stat_day.columns=['_'.join(col).strip() for col in df_stat_day.columns.values ]
            return df_stat_day
        
        if typ == 'month':
            df_stat_month=df_log.groupby(['month']).agg({'操作人':['nunique','count'] }).reset_index()
            df_stat_month.columns=['_'.join(col).strip() for col in df_stat_month.columns.values ]
            df_stat_month=df_stat_month.rename(columns={'month_':'date_'})
            
            return df_stat_month
        
    
    else:
        
        if typ == 'day': 
            #log contain labels
            df_analysis=df_log[df_log['操作日志'].str.contains(log_label) == True].reset_index(drop=True)
            df_analysis.rename(columns = {'操作人':log_label}, inplace = True)
            df_stat_day=df_analysis.groupby(['date']).agg({log_label:['nunique','count'] }).reset_index()
            
            df_stat_day.columns=['_'.join(col).strip() for col in df_stat_day.columns.values ]  
            
            

            return df_stat_day

        if typ == 'month':
            df_analysis=df_log[df_log['操作日志'].str.contains(log_label) == True].reset_index(drop=True)
            df_analysis.rename(columns = {'操作人':log_label}, inplace = True)
            df_stat_month=df_analysis.groupby(['month']).agg({log_label:['nunique','count'] }).reset_index()
            df_stat_month.columns=['_'.join(col).strip() for col in df_stat_month.columns.values ] 
            df_stat_month=df_stat_month.rename(columns={'month_':'date_'})
            
            
            return df_stat_month
         

st.title('ETP使用数据')

st.subheader('总体日活')

df_log_daily=log_stat('day','all')
fig = px.line(df_log_daily,x='date_',y='操作人_nunique')
st.plotly_chart(fig, use_container_width=True)

st.subheader('总体月活')

df_log_monthly=log_stat('month','all')
fig = px.line(df_log_monthly,x='date_',y='操作人_nunique')
st.plotly_chart(fig, use_container_width=True)

