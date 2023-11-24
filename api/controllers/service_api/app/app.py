# -*- coding:utf-8 -*-
from flask_restful import fields, marshal_with
from flask import current_app

from controllers.service_api import api
from controllers.service_api.wraps import AppApiResource

from models.model import App


class AppParameterApi(AppApiResource):
    """Resource for app variables."""

    variable_fields = {
        'key': fields.String,
        'name': fields.String,
        'description': fields.String,
        'type': fields.String,
        'default': fields.String,
        'max_length': fields.Integer,
        'options': fields.List(fields.String)
    }

    system_parameters_fields = {
        'image_file_size_limit': fields.String
    }

    parameters_fields = {
        'opening_statement': fields.String,
        'suggested_questions': fields.Raw,
        'suggested_questions_after_answer': fields.Raw,
        'speech_to_text': fields.Raw,
        'retriever_resource': fields.Raw,
        'more_like_this': fields.Raw,
        'user_input_form': fields.Raw,
        'sensitive_word_avoidance': fields.Raw,
        'file_upload': fields.Raw,
        'system_parameters': fields.Nested(system_parameters_fields)
    }

    # @marshal_with(parameters_fields)
    def get(self, app_model: App, end_user):
        """Retrieve app parameters."""
        app_model_config = app_model.app_model_config

        return {
            'opening_statement': app_model_config.opening_statement,
            'suggested_questions': app_model_config.suggested_questions_list,
            'suggested_questions_after_answer': app_model_config.suggested_questions_after_answer_dict,
            'speech_to_text': app_model_config.speech_to_text_dict,
            'retriever_resource': app_model_config.retriever_resource_dict,
            'more_like_this': app_model_config.more_like_this_dict,
            'user_input_form': app_model_config.user_input_form_list,
            'sensitive_word_avoidance': app_model_config.sensitive_word_avoidance_dict,
            'file_upload': app_model_config.file_upload_dict,
            'system_parameters': {
                'image_file_size_limit': current_app.config.get('UPLOAD_IMAGE_FILE_SIZE_LIMIT')
            },
            'pre_prompt': app_model_config.pre_prompt,
            'prompt_type': app_model_config.prompt_type,
            'chat_prompt_config': app_model_config.chat_prompt_config,
            'completion_prompt_config': app_model_config.completion_prompt_config,
        }
        # 将app_model_config转换为json
        

api.add_resource(AppParameterApi, '/parameters')
