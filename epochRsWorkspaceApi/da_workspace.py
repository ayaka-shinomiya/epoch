#   Copyright 2019 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import json

import globals
from dbconnector import dbcursor

def insert_workspace(cursor, specification):
    """workspace情報登録

    Args:
        cursor (mysql.connector.cursor): カーソル
        specification (Dict)): ワークスペース情報のJson形式

    Returns:
        int: ワークスペースID
        
    """
    # insert実行
    cursor.execute('INSERT INTO workspace ( organization_id, specification ) VALUES ( 1, %(specification)s )',
        {
            'specification' : json.dumps(specification)
        }
    )
    # 追加したワークスペースIDをreturn
    return cursor.lastrowid

def update_workspace(cursor, specification, workspace_id):
    """workspace情報更新

    Args:
        cursor (mysql.connector.cursor): カーソル
        specification (Dict)): ワークスペース情報のJson形式

    Returns:
        int: アップデート件数
        
    """
    # workspace情報 update実行
    upd_cnt = cursor.execute('UPDATE workspace SET specification = %(specification)s WHERE workspace_id = %(workspace_id)s',
        {
            'workspace_id' : workspace_id,
            'specification': json.dumps(specification)
        }
    )
    # 更新した件数をreturn
    return upd_cnt

def patch_workspace(cursor, workspace_id, role_date_at, json):
    """workspace情報更新パッチ

    Args:
        cursor (mysql.connector.cursor): カーソル
        specification (Dict)): ワークスペース情報のJson形式
        role_date_at (Date)): role update date

    Returns:
        int: アップデート件数
        
    """
    data = []
    for key in json:
        # JSON整形
        data.append(
            {
                str(key) : json[str(key)].values()
            }
        )

    # UPDATE文の”role_date_at”の部分を整形したkeyの数だけ置き換える（未実装）
    
    # workspace情報 update実行
    upd_cnt = cursor.execute('UPDATE workspace SET role_date_at = %(role_date_at)s WHERE workspace_id = %(workspace_id)s', data)
    
    # 更新した件数をreturn
    return upd_cnt
    

def select_workspace_id(cursor, workspace_id):
    """workspace情報取得(id指定)

    Args:
        cursor (mysql.connector.cursor): カーソル
        workspace_id (int): ワークスペースID

    Returns:
        dict: select結果
    """
    # select実行
    cursor.execute('SELECT * FROM workspace WHERE workspace_id = %(workspace_id)s ORDER BY workspace_id',
        {
            'workspace_id' : workspace_id
        }
    )
    rows = cursor.fetchall()
    return rows

def select_workspace(cursor):
    """workspace情報取得(全取得)

    Args:
        cursor (mysql.connector.cursor): カーソル

    Returns:
        dict: select結果
    """
    # select実行
    cursor.execute('SELECT * FROM workspace ORDER BY workspace_id')
    rows = cursor.fetchall()
    return rows

def insert_history(cursor, workspace_id):
    """workspace履歴情報追加

    Args:
        cursor (mysql.connector.cursor): カーソル
        workspace_id (int): ワークスペースID
    """
    cursor.execute(
        '''INSERT INTO workspace_history (workspace_id, organization_id, update_at, role_update_at, specification)
            SELECT workspace_id, organization_id, update_at, role_update_at, specification FROM workspace WHERE workspace_id = %(workspace_id)s''',
        {
            'workspace_id' : workspace_id
        }
    )

