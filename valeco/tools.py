def range_bar(N):
    '''
    Progress bar within a range.
    :param N:
    :return:

    .. Warning: need to install
                `jupyter labextension install ipyvolume`
            and
                `jupyter labextension install @jupyter-widgets/jupyterlab-manager`

    ..exemple::
        >>> import time
        >>> from pydap.tool.progress import range_bar
        >>> for i in range_bar(100):
        >>>     time.sleep(0.1)
        >>>
    '''



    from ipywidgets import IntProgress
    from IPython.display import display
    import time

    pbar = IntProgress(
        value=0,
        min=0,
        max=N,
        step=1,
        description='Loading:',
        bar_style='',  # 'success', 'info', 'warning', 'danger' or ''
        orientation='horizontal'
    )
    display(pbar)  # display the bar

    start_time = time.time()
    for k in range(N):
        loc_time = int(time.time() - start_time)
        if loc_time < 10 * 60:
            # Formatage MM'SS'' si temps inférieur à 10'
            str_time = f"{loc_time // 60:3}'{loc_time % 60:2}''"
        else:
            str_time = f"{loc_time // 60}'"

        pbar.value += 1  # signal to increment the progress bar
        pbar.description = f"{str_time}: {int(k / N * 100):3}%"
        if k == N - 1:
            pbar.description = f"{str_time}"
        yield k
