"""Create an extended fictional consulting company for end-to-end examples."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
from create_fixture import fixture


def extended():
    data=fixture(); data['schema_version']='1.0'
    base={'company_id':data['company']['id'],'metadata':deepcopy(data['company']['metadata'])}
    data['entities']=[
        {**deepcopy(base),'id':'goal-delivery','record_type':'Goal','name':'Improve project margin','metric':'project_margin','target':'0.5','direction':'at_least','due_date':'2026-11-30'},
        {**deepcopy(base),'id':'project-launch','record_type':'Project','name':'Client launch','goal_id':'goal-delivery','status':'blocked'},
        {**deepcopy(base),'id':'task-review','record_type':'Task','name':'Confirm delivery scope','project_id':'project-launch','owner':'founder','status':'todo','due_date':'2026-11-06'},
        {**deepcopy(base),'id':'customer-demo','record_type':'Customer','name':'Fictional prospective customer','stage':'qualified','value':'5000.00'},
        {**deepcopy(base),'id':'product-audit','record_type':'Product','name':'Strategy audit','price':'2000.00','unit_cost':'800.00','status':'active'},
        {**deepcopy(base),'id':'campaign-demo','record_type':'Campaign','name':'Fictional acquisition test','product_id':'product-audit','channel':'newsletter','budget':'500.00','status':'active'},
    ]
    data['measurements']=[]
    for metric,value,unit in [('project_revenue','2000.00','money'),('delivery_cost','800.00','money'),('billable_hours','24','hours'),('available_hours','40','hours'),('incremental_revenue','1200.00','money')]:
        data['measurements'].append({**deepcopy(base),'id':'measure-'+metric,'record_type':'Measurement','metric':metric,
                                     'value':value,'unit':unit,'start':'2026-11-02','end':'2026-11-08'})
    data['custom_kpis']=[{'name':'cash_margin','formula':'profit/revenue','input_units':{'profit':'money','revenue':'money'},'unit':'ratio','description':'Cash-basis profit margin'}]
    return data


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('output',type=Path); args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x',encoding='utf-8') as file: json.dump(extended(),file,indent=2); file.write('\n')
