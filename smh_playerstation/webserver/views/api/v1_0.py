# -*- coding: utf-8 -*-

import json

from flask import jsonify, request, send_from_directory, make_response

from .. import status


class V1_0(object):

    def __init__(self, app, url_prefix, playerstation):
        self.app = app
        self.url_prefix = url_prefix
        self.ps = playerstation
        self.ROUTES = {
            # Basic
            '/description': {
                'view_func': self.description_get,
                'methods': ['GET']
            },
            '/status': {
                'view_func': self.status_get,
                'methods': ['GET'],
            },
            '/shutdown': {
                'view_func': self.shutdown_get,
                'methods': ['GET'],
            },
            # Songs
            '/songs': {
                'view_func': self.songs_get,
                'methods': ['GET'],
            },
            '/songs/scan': {
                'view_func': self.songs_scan_get,
                'methods': ['GET'],
            },
            '/songs/rescan': {
                'view_func': self.songs_rescan_get,
                'methods': ['GET'],
            },
            '/songs/youtube': {
                'view_func': self.songs_youtube_get,
                'methods': ['GET'],
            },
            '/songs/youtube/download': {
                'view_func': self.songs_youtube_download_post,
                'methods': ['POST'],
            },
            # Player
            '/player': {
                'view_func': self.player_get,
                'methods': ['GET'],
            },
            '/player/playlist': {
                'view_func': self.player_playlist,
                'methods': ['POST', 'PUT'],
            },
            '/player/mode/<mode>': {
                'view_func': self.player_mode_post,
                'methods': ['POST'],
            },
            '/player/action/<action>': {
                'view_func': self.player_action_get,
                'methods': ['GET'],
            },

            # Playlists
        }
        for k, v in self.ROUTES.items():
            app.add_url_rule(
                rule=self.url_prefix + k,
                endpoint='api_v1_0_' + v['view_func'].__name__,
                **v
            )

    #
    # # Basic
    #
    def description_get(self):
        """Show API usage."""
        retval = {
            'service': 'smh_playerstation',
            'URL prefix': self.url_prefix,
            'description': 'REST API to control the smh_playerstation',
            'methods': {
                k: {
                    'methods': v['methods'],
                    'description': v['view_func'].__doc__,
                }
                for k, v in self.ROUTES.items()
            }
        }
        return(jsonify(retval), status.OK)

    def status_get(self):
        """Information  of the different components of the smh_playerstation."""
        ps_status = {
            'player': self.ps.player.status(),
            'workers': self.ps.workers.status()
        }
        return(jsonify(ps_status), status.OK)

    def shutdown_get(self):
        """Shutdown (safely) the server."""
        self.ps.stop()
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    #
    # # Songs
    #
    def songs_get(self):
        """List all the available songs.
        """
        retval = self.ps.songs.songs_list
        return(jsonify(retval), status.OK)

    def songs_scan_get(self):
        """Find new songs in the collection (fast).
        """
        self.ps.songs.scan_new_songs()
        retval = 'OK'
        return(jsonify(retval), status.OK)

    def songs_rescan_get(self):
        """Re-index the whole collection (slow).
        """
        self.ps.songs.rescan_collection()
        retval = 'OK'
        return(jsonify(retval), status.OK)

    def songs_youtube_get(self):
        """List all the Youtube song ids.
        """
        retval = list(self.ps.songs.youtube_ids)
        return(jsonify(retval), status.OK)

    def songs_youtube_download_post(self):
        """Download songs from Youtube and add it to the collection.
        """
        # POST params
        youtube_ids = request.form.get('youtube_ids').split()
        path = request.form.get('path', '')
        if not youtube_ids:
            return(
                jsonify({'error': 'youtube_id param required.'}),
                status.BAD_REQUEST
            )
        for youtube_id in youtube_ids:
            self.ps.songs.download_from_youtube(
                youtube_id=youtube_id,
                path=path
            )
        return(jsonify('OK'), status.OK)

    #
    # # Player
    #
    def player_get(self):
        """Show the status of the player: playlist, position, mode, etc.
        """
        retval = self.ps.player.status()
        return(jsonify(retval), status.OK)

    def player_playlist(self):
        """Extend or replace the player playlist.
        """
        song_ids = json.loads(request.form.get('song_ids'))
        if not song_ids:
            return(
                jsonify({'error': 'song_ids param required.'}),
                status.BAD_REQUEST
            )
        if request.method == 'POST':
            self.ps.player.add_list(files=song_ids)
        elif request.method == 'PUT':
            self.ps.player.set_list(files=song_ids)
        return(jsonify('OK'), status.OK)

    def player_action_get(self, action):
        """Control the player.
        """
        print(action)
        retval = (jsonify('OK'), status.OK)
        if action == "play":
            self.ps.player.play()
        elif action == "play_next":
            self.ps.player.play_next()
        elif action == "stop":
            self.ps.player.stop()
        else:
            retval = (
                {'error': 'action MUST be: play, play_next or stop'},
                status.BAD_REQUEST
            )
        return(retval)

    def player_mode_post(self, mode):
        """Set the player mode.
        """
        if mode in self.ps.player.MODES:
            retval = (jsonify('OK'), status.OK)
            self.ps.player.set_mode(mode)
        else:
            retval = (jsonify({'error': 'mode not found'}), status.BAD_REQUEST)
        return retval

    #
    # # Playlists
    #






    # #@crossdomain(origin='*')
    # def job_get(self,job_id):
    #     job = Job.from_db(self.db,job_id)
    #     if job: #Filter what to return
    #         retval = {
    #             k:v
    #             for k,v in job.job_doc.iteritems()
    #             if k in ['id','status','log','waiting_user']
    #         }
    #         return(jsonify(retval))
    #     else:
    #         return(
    #             jsonify({'error': 'Job id not found.'}),
    #             status.NOT_FOUND
    #         )
    #
    #
    # #@crossdomain(origin='*')
    # def job_post(self):
    #     #Check input
    #     files = {}
    #     files_params = {}
    #     for fk in Job.INPUT_FILES.keys():
    #         files[fk] = request.files.get('file_{0}'.format(fk))
    #         if not files[fk]:
    #             return(
    #                 jsonify({'error': 'No file_{0} provided.'.format(fk)}),
    #                 status.BAD_REQUEST
    #             )
    #         files_params[fk] = json.loads(
    #             request.form.get('file_{0}_params'.format(fk))
    #         )
    #         if not files_params[fk]:
    #             return(
    #                 jsonify({'error': 'No file_{0}_params provided.'.format(fk)}),
    #                 status.BAD_REQUEST
    #             )
    #     parameters = json.loads(request.form.get('parameters'))
    #     if not parameters:
    #         return(
    #             jsonify({'error': 'No parameters provided.'}),
    #             status.BAD_REQUEST
    #         )
    #     #Build arguments to create a job.
    #     job_files = {}
    #     for fk,fv in Job.INPUT_FILES.items():
    #         job_files[fk] = {
    #             k:(files_params[fk].get(k) or v)
    #             for k,v in fv['params'].items()
    #         }
    #         job_files[fk]['path'] = self._save_file(files[fk])
    #         job_files[fk]['original_name'] = files[fk].filename
    #         job_files[fk]['bytes'] = os.path.getsize(job_files[fk]['path'])
    #
    #     job = Job.create(
    #         db=self.db,
    #         file_clients=job_files['clients'],
    #         file_segments=job_files['segments'],
    #         parameters=parameters
    #     )
    #     job.start(self.celery) #Start asynchronous process
    #     return(
    #         jsonify({'job_id':job.job_doc['id']}),
    #         status.CREATED
    #     )
    #
    #
    # #@crossdomain(origin='*')
    # def job_export(self, job_id, job_status):
    #     # Get job and check status
    #     job = Job.from_db(self.db,job_id)
    #     if job_status not in job.job_doc['log']:
    #         return(
    #             jsonify({
    #                 'error': 'job has not reached the status {0}.'.format(job_status)
    #             }),
    #             status.BAD_REQUEST
    #         )
    #     # Get clients and select fields to retrieve
    #     clients = model.Clients(None,job_id,self.db).get()
    #     FIELDS = ['ID','LONGITUDE','LATITUDE']
    #     if job_status == Job.STATUS_TERRITORY_FINISHED:
    #         FIELDS.extend(['TM'])
    #     elif job_status == Job.STATUS_DAY_FINISHED:
    #         FIELDS.extend(['TM','DAY'])
    #     elif job_status == Job.STATUS_WEEK_FINISHED:
    #         FIELDS.extend(['TM','DAY'])
    #         FIELDS.extend([  # Add weeks
    #             w
    #             for w in clients[0].keys()
    #             if w.startswith('week')
    #         ])
    #     elif job_status == Job.STATUS_SEQUENCE_FINISHED:  # Deliverable
    #         FIELDS.extend(['TM','DAY'])
    #         FIELDS.extend([  # Add weeks and sequences
    #             w
    #             for w in clients[0].keys()
    #             if w.startswith('week') or w.startswith('seq')
    #         ])
    #     else:
    #         return (
    #             jsonify({'error': 'status not exportable.'}),
    #             status.BAD_REQUEST
    #         )
    #     # Build CSV
    #     csv = cStringIO.StringIO()
    #     dwriter = DictWriter(csv, fieldnames=FIELDS, extrasaction='ignore')
    #     dwriter.writeheader()
    #     dwriter.writerows(clients)
    #     # Return a CSV file
    #     response = make_response(csv.getvalue())
    #     response.headers["Content-Disposition"] = "attachment; filename={status}_{id}.csv".format(
    #         status=job_status, id=job_id
    #     )
    #     return response
    #
    #
    # #@crossdomain(origin='*')
    # def job_resume(self, job_id, job_status):
    #     # Get job and check status
    #     job = Job.from_db(self.db,job_id)
    #     if job_status not in job.job_doc['log']:
    #         print 'err1'
    #         return(
    #             jsonify({
    #                 'error': 'job has not reached the status {0}.'.format(job_status)
    #             }),
    #             status.BAD_REQUEST
    #         )
    #     if not job.job_doc['waiting_user']:
    #         print 'err2'
    #         return(
    #             jsonify({
    #                 'error': 'job is already queued.'
    #             }),
    #             status.BAD_REQUEST
    #         )
    #
    #     # Set resume function
    #     resume_func = {
    #         Job.STATUS_TERRITORY_FINISHED: job.resume_day,
    #         Job.STATUS_DAY_FINISHED: job.resume_week,
    #         Job.STATUS_WEEK_FINISHED: job.resume_sequence
    #     }
    #     if job_status not in resume_func:
    #         print 'err3'
    #         return (
    #             jsonify({'error': 'status not resumable.'}),
    #             status.BAD_REQUEST
    #         )
    #     # Update fields
    #     file_resume = request.files.get('file_resume')
    #     if file_resume:
    #         with open(file_resume, 'r') as f_csv:
    #             csv = DictReader(f_csv)
    #             fields = {
    #                 Job.STATUS_TERRITORY_FINISHED: ['TM'],
    #                 Job.STATUS_DAY_FINISHED: ['DAY'],
    #                 Job.STATUS_WEEK_FINISHED: [
    #                     w for w in csv.fieldnames
    #                     if w.startswith('week')
    #                 ]
    #             }
    #             data = { field:[] for field in fields[job_status]}
    #             data['ID'] = []  # Indexing field
    #             for row in csv:
    #                 for field in data.keys():
    #                     data[field].append(row[field])
    #         clients = model.Clients(None,job_id,self.db)
    #         for field in fields[job_status]:
    #             clients.add_field_values(
    #                 name=field,
    #                 values=data[field],
    #                 index_field='ID',
    #                 index_values=data['ID']
    #             )
    #     print 'resume job: {0}-{1}'.format(job_id, job_status)
    #     try:
    #         resume_func[job_status](self.celery)  # Resume job
    #     except Exception as e:
    #         print e.message
    #     return(
    #         jsonify({
    #             'job_id':job.job_doc['id'],
    #             'resumed_from':job_status
    #         }),
    #         status.OK
    #     )
