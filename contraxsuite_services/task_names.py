"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
# -*- coding: utf-8 -*-


__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2020, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.6.0/LICENSE"
__version__ = "1.6.0"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


TASK_NAME_AUTO_REINDEX = 'apps.rawdb.tasks.auto_reindex'

TASK_NAME_MANUAL_REINDEX = 'RawDB: Reindex'

TASK_NAME_UPDATE_PROJECT_DOCUMENTS = 'RawDB: Update project documents'

TASK_NAME_UPDATE_ASSIGNEE_FOR_DOCUMENTS = 'RawDB: Update assignee for documents'

TASK_NAME_UPDATE_STATUS_NAME_FOR_DOCUMENTS = 'RawDB: Update status name for documents'

TASK_NAME_IMANAGE_TRIGGER_SYNC = 'apps.imanage_integration.tasks.trigger_imanage_sync'

TASK_NAME_TRIGGER_DIGESTS = 'apps.notifications.tasks.trigger_digests'

TASK_NAME_CHECK_EMAIL_POOL = 'apps.notifications.tasks.check_email_pool'

TASK_NAME_TRACK_TASKS = 'advanced_celery.track_tasks'

TASK_NAME_TRACK_FAILED_TASKS = 'advanced_celery.track_failed_tasks'

TASK_NAME_UPDATE_PARENT_TASK = 'advanced_celery.update_parent_task'

TASK_NAME_CLEAN_TASKS_PERIODIC = 'advanced_celery.clean_tasks_periodic'

TASK_NAME_RETRAIN_DIRTY_TASKS = 'advanced_celery.retrain_dirty_fields'

TASK_NAME_CACHE_UPDATED_DOCS = 'advanced_celery.cache_updated_docs'

TASK_NAME_TRACK_SESSION_COMPLETED = 'advanced_celery.track_session_completed'

TASK_NAME_USAGE_STATS = 'deployment.usage_stats'

TASK_NAME_CACHE_DOC_NOT_TRACKED = 'apps.rawdb.tasks.cache_document_fields_for_doc_ids_not_tracked'

TASK_NAME_UPDATE_MAIN_TASK = 'advanced_celery.update_main_task'

TASK_NAME_NOTIFICATIONS_ON_DOCUMENT_CHANGE = 'apps.notifications.tasks.process_notifications_on_document_change'

TASK_NAME_DELETE_METHOD_STATS = 'apps.common.tasks.delete_method_stats'

TASK_NAME_INIT_METHOD_STATS_COLLECTORS = 'apps.common.tasks.init_method_stats_collectors'

TASK_NAME_IDENTIFY_CONTRACTS = 'Identify Contracts'

TASK_NAME_MONITOR_DISK_USAGE = 'advanced_celery.monitor_disk_usage'

TASK_NAME_PLAN_REFRESHING_MATERIALIZED_VIEWS = 'apps.materialized_views.tasks.plan_refreshing_materialized_views'

TASK_NAME_REFRESH_MATERIALIZED_VIEW = 'apps.materialized_views.tasks.refresh_materialized_view'

TASK_FRIENDLY_NAME = {
    TASK_NAME_CLEAN_TASKS_PERIODIC: 'Clean Tasks Periodically',
    TASK_NAME_RETRAIN_DIRTY_TASKS: 'Retrain Dirty Fields',
    TASK_NAME_CACHE_UPDATED_DOCS: 'Cache Updated Documents',
    TASK_NAME_TRACK_FAILED_TASKS: 'Track Failed Tasks',
    TASK_NAME_TRACK_SESSION_COMPLETED: 'Track Session Completed',
    TASK_NAME_TRACK_TASKS: 'Track Tasks',
    TASK_NAME_DELETE_METHOD_STATS: 'Delete Method Stats',
    TASK_NAME_INIT_METHOD_STATS_COLLECTORS: 'Init Method Stats Collectors',
    'apps.document.async_tasks.detect_field_values_task.detect_field_values_for_document': 'Detect Field Values On Document (async)',
    'apps.document.tasks.detect_field_values_for_document': 'Detect Field Values On Document',
    TASK_NAME_IMANAGE_TRIGGER_SYNC: 'IManage: Trigger Sync',
    TASK_NAME_CHECK_EMAIL_POOL: 'Check Email Pool',
    'manual_reindex': 'Manual Reindex',
    'index_documents': 'Index Documents',
    'detect_field_values_for_document': 'Detect Field Values',
    'apps.task.tasks.create_document': 'Create Document',
    'apps.task.tasks.create_document_from_bytes': 'Create Document From Bytes',
    'apps.task.tasks.parse_text_units': 'Parse Text Units',
    'auto_reindex_not_tracked': 'Auto Reindex Not Tracked',
    'process_document_changed': 'Process Document Changed',
    'process_documents_status_changed': 'Process Document Status Changed',
    TASK_NAME_NOTIFICATIONS_ON_DOCUMENT_CHANGE: 'Notify On Document Changed',
    'process_notifications_on_document_change': 'Notify On Document Changed',
    TASK_NAME_AUTO_REINDEX: 'Auto Reindex',
    TASK_NAME_TRIGGER_DIGESTS: 'Trigger Digests',
    'apps.task.tasks.on_locate_finished': 'On Locate Finished',
    'apps.task.tasks.delete_document_on_load_failed': 'Delete Document On Load Failed',
    'apps.rawdb.tasks.cache_document_fields_for_doc_ids_tracked': 'Cache Document Fields (for doc ids tracked)',
    'apps.task.tasks.clean_tasks': 'Clean All Tasks',
    TASK_NAME_REFRESH_MATERIALIZED_VIEW: 'Refresh Materialized View'
}
