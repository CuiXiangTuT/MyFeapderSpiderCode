from feapder.pipelines import BasePipeline
from typing import Dict, List, Tuple
from setting import *
from feapder.db.mysqldb import MysqlDB
from feapder.utils import tools
from feapder.utils.log import log


class HkTemporaryDataInstagramInfoPipeline(BasePipeline):
    def __init__(self) -> None:
        # 链接数据库
        self._db = MysqlDB(ip=MYSQL_IP,
                           port=MYSQL_PORT,
                           user_name=MYSQL_USER_NAME,
                           user_pass=MYSQL_USER_PASS,
                           db=MYSQL_DB)

    def save_items(self, table, items: List[Dict]) -> bool:
        """
        保存数据
        Args:
            table: 表名
            items: 数据，[{},{},...]

        Returns: 是否保存成功 True / False
                 若False，不会将本批数据入到去重库，以便再次入库

        """

        sql, datas = tools.make_batch_sql(table, items)
        add_count = self._db.add_batch(sql, datas)
        datas_size = len(datas)
        if add_count:
            log.debug("共导出 %s 条数据 到 %s, 重复 %s 条" %
                      (datas_size, table, datas_size - add_count))
        return add_count != None

    def update_items(self,
                     table,
                     items: List[Dict],
                     update_keys=Tuple) -> bool:
        """
        更新数据
        Args:
            table: 表名
            items: 数据，[{},{},...]
            update_keys: 更新的字段, 如 ("title", "publish_time")

        Returns: 是否更新成功 True / False
                 若False，不会将本批数据入到去重库，以便再次入库
        """

        sql, datas = tools.make_batch_sql(table,
                                          items,
                                          update_columns=update_keys
                                          or list(items[0].keys()))
        update_count = self._db.add_batch(sql, datas)
        if update_count:
            msg = "共更新 %s 条数据 到 %s" % (update_count // 2, table)
            if update_keys:
                msg += " 更新字段为 {}".format(update_keys)
            log.debug(msg)
        return update_count != None
